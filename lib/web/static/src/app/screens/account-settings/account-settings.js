import angular from 'angular';

import  { appApi } from '../../api/app.api';

import { AccountSettingsScreen } from './account-settings.screen';

export let accountSettingsScreen = angular
  .module('agilecrm-app.accountSettingsScreen', [
    appApi
  ])
  .component('accountSettingsScreen', AccountSettingsScreen)
  .name;