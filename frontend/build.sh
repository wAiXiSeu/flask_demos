#!/usr/bin/env bash
echo "dist generating"
rm -rf ./dist
npm run build
echo "dist generated"
