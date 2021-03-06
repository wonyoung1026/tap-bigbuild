# -*- coding: utf-8 -*-
import os

from invoke import task, run

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')


@task
def test(ctx):
    run('python3 setup.py test', pty=True)


@task
def clean(ctx):
    run('rm -rf build')
    run('rm -rf dist')
    run('rm -rf bigbuild.egg-info')
    run('rm -rf __pycache__')
    run('rm -rf .pytest_cache')
    run('rm -rf .eggs')


    clean_docs(ctx)
    print("Cleaned up.")


@task
def clean_docs(ctx):
    run('rm -rf %s' % build_dir)


@task
def browse_docs(ctx):
    run('open %s' % os.path.join(build_dir, 'index.html'))


@task
def build_docs(ctx, clean=False, browse=False):
    if clean:
        clean_docs(ctx)
    run('sphinx-build %s %s' % (docs_dir, build_dir), pty=True)
    if browse:
        browse_docs(ctx)


@task
def readme(ctx, browse=False):
    run('rst2html.py README.rst > README.html')


@task
def publish(ctx, test=False):
    """Publish to the cheeseshop."""
    if test:
        run('python3 setup.py register -r test sdist upload -r test')
    else:
        run("python3 setup.py register sdist upload")

@task
def build(c, docs=False):
    c.run("python3 setup.py build")
    if docs:
        c.run("sphinx-build docs docs/_build")

@task
def install(c):
    c.run("python3 setup.py install")