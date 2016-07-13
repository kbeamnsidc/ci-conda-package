import os

from invoke import run, task

from tasks import hack


def get_package_info():
    """
    read the package information from the conda build artifact
    """

    with open(hack.CONDA_ARTIFACT_FILENAME, 'r') as fn:
        pkg_location = fn.read().strip()
        pkg_name = os.path.basename(pkg_location)

    return pkg_location, pkg_name


@task()
def assert_new_package(channel, package):
    """Verify current version of package does not already exist in the desired channel.

    This is just a sanity check to make sure you haven't forgotten to
    bumpversion.  If you have, then you've likely got a new package on dev, with
    vX.Y.Zdev and vX.Y.Z on dev channel and already have a vX.Y.Z on main.

    Also, you can't just use an API to see if a package exists, that's why
    the grep stuff is in here.

    When you get this error, the most likely thing to do is, remove your dev
    channel packages, then bumpversion and try again.

    """
    test_version = hack.current_version()
    cmd = ('conda search --override-channels '
           '--channel http://conda.anaconda.org/nsidc/channel/{channel} '
           ' {package} | grep {test_version}')
    ret_value = run(
        cmd.format(channel=channel, package=package, test_version=test_version),
        hide=True, warn=True)

    # success from the grep means that the package is already there, so we
    # want to fail...
    if ret_value.ok is True:
        raise RuntimeError('Package {}=={} exists on {}, '
                           'either: delete from anaconda.org (unlikely) or '
                           'bump your version and try again '
                           'before continuing.'.format(package, test_version, channel))


@task(default=True)
def anaconda(channel, token):
    """
    deploy package to anaconda.org
    """

    pkg_location, pkg_name = get_package_info()
    pkg_dir, _ = os.path.split(pkg_location)
    pkg_root = pkg_dir.replace('linux-64', '')

    osx_location = pkg_location.replace('linux-64', 'osx-64')

    cmd = 'anaconda -t {token} upload -u nsidc {location} -c {channel} --force && '
    cmd += 'conda convert {location} -p osx-64 -o {root} &&'
    cmd += 'anaconda -t {token} upload -u nsidc {osx_location} -c {channel} --force'
    run(cmd.format(location=pkg_location,
                   name=pkg_name,
                   channel=channel,
                   root=pkg_root,
                   token=token,
                   osx_location=osx_location))
