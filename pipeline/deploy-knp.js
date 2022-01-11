'use strict';
const settings = require('./lib/config.js')
const task = require('./lib/deploy-knp.js')

task(Object.assign(settings, { phase: settings.options.env}));
