import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { ConfigurationService } from './configuration.service';
import { Config } from '../interfaces/config';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  httpClient = inject(HttpClient);
  configService = inject(ConfigurationService);
  config!: Config;

  constructor() {
    this.config = this.configService.getConfig();
  }

  

}
