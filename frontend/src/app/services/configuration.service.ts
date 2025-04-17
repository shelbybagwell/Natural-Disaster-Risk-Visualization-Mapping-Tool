import { Injectable } from '@angular/core';
import * as configJSON from '../../../config.json';
import { Config } from '../interfaces/config';

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {
  config!: Config;

  constructor() { }

  getConfig() {
    configJSON.map(item => {
      apiBaseUrl: item.localConfig.apiBaseUrl
    })
  }
}
