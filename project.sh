#!/usr/bin/env bash

. config/.project

error() {
    echo $1
    exit 1
}

help() {
    echo "Project management script"
    echo "usage: $0 <command> [<options>]"
    echo "These are common project commands:"
    echo "build         Build project release"
    echo ""
}

python() {
    interp=$1
    if [ -z $interp ]; then
        interp=python
    fi
    PY=`which $interp`
    if [ -z $PY ]; then
        error "Invalid iterpreter $PY"
    fi
}

npm() {
    interp=$1
    if [ -z $interp ]; then
        interp=npm
    fi
    NPM=`which $interp`
    if [ -z $NPM ]; then
        error "Invalid npm $NPM"
    fi
}

sqitch() {
    local URI="db:$1"
    SQITCH=`which sqitch`
    if [ -z $SQITCH ]; then
       error "Cannot find sqitch command in your PATH $PATH"
    fi
    SQITCH="$SQITCH --quiet --top-dir migrations/ --engine pg"
    $SQITCH deploy $URI > /dev/null
}

build() {
    if [ $# -lt 1 ]; then
        error "$0 build <python interpreter> <stage>"
    fi
    python $1
    if [ $2 ]; then
        STAGE=$2
    fi
    echo "Build project $PROJECT stage $STAGE interpreter $PY"
    echo "[versions]
setuptools=$setuptools_version
zc.buildout=$buildout_version" > config/buildout/bootstrap.cfg
    echo "[buildout]
extends = config/buildout/$STAGE.cfg" > buildout.cfg
    $PY sutils/bootstrap.py --setuptools-version=$setuptools_version --buildout-version=$buildout_version && \
        ./bin/buildout
}

assets() {
    npm $1
    if [ ! -d assets ]; then
        mkdir -p assets
    fi
    if [ ! -f assets/manifest.json ]; then
        echo '{}' > assets/manifest.json
    fi
    $NPM i && \
    $NPM run assets
}

deploy() {
    URI=`grep 'SQLALCHEMY_DATABASE_URI' config/flask/$STAGE.cfg | awk '{print $NF}' | sed "s#'##g"`
    sqitch $URI
}

case "$1" in
    build)
        build $2 $3
        ;;
    assets)
        assets $2
        ;;
    deploy)
        deploy
        ;;
    *)
        if [ $1 ]; then
            echo "Invalid action: $1"
        fi
        echo ""
        help
        ;;
esac
