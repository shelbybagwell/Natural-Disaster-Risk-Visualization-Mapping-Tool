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
      this.config.apiBaseUrl = item.localConfig.apiBaseUrl
    });
    return this.config;
  }
}
