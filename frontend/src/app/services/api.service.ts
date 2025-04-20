import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { ConfigurationService } from './configuration.service';
import { Config } from '../interfaces/config';
import { catchError, Observable, throwError } from 'rxjs';
import { Address } from '../interfaces/address';

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

  private handleErrors(error: HttpErrorResponse) {
    let message = 'An unknown error occurred';
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      message = `Error: ${error.error.message}`;
    } else if (error.status) {
      // Server-side error
      message = `Error ${error.status}: ${error.message}`;
    }
    return throwError(() => new Error(message));
  }

  // Get all addresses, and do not consider user ID
  getAllAddresses<T>(params?:  HttpParams): Observable<T> {
    return this.httpClient.get<T>(
      `${this.config.apiBaseUrl}/search`, {
      params
    })
    .pipe(catchError(this.handleErrors));
  }

  // get all User Addresses
  getUserAddresses<T>(user: string, params?: HttpParams): Observable<T> {
    return this.httpClient.get<T>(
      `${this.config.apiBaseUrl}/list/user/${user}`, {
      params
    })
    .pipe(catchError(this.handleErrors));
  }

  // get address by ID
  getSpecifcAddresses<T>(addressID: string, params?: HttpParams): Observable<T> {
    return this.httpClient.get<T>(
      `${this.config.apiBaseUrl}/${addressID}`, {
      params
    })
    .pipe(catchError(this.handleErrors));
  }

  // Add User Address
  addUserAddress<T>(user: string, body: Address): Observable<T> {
    return this.httpClient.put<T>(
      `${this.config.apiBaseUrl}/user/${user}`, 
      body
    )
    .pipe(catchError(this.handleErrors));
  }

  // Update User Address
  updateUserAddress<T>(addressID: string, body: Address): Observable<T> {
    return this.httpClient.put<T>(
      `${this.config.apiBaseUrl}/${addressID}`,
      body,
    )
    .pipe(catchError(this.handleErrors));
  }

  // Delete User Address
  deleteUserAddress<T>(addressID: string): Observable<T> {
    return this.httpClient.delete<T>(
      `${this.config.apiBaseUrl}/${addressID}`
    )
    .pipe(catchError(this.handleErrors));
  }

  

}
