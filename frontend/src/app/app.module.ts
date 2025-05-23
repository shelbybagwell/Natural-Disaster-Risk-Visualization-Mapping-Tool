import { importProvidersFrom, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS, HttpClientModule, provideHttpClient, withInterceptors } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MapContainerComponent } from './components/maps/map-container/map-container.component';
import { HeaderComponent } from './components/layout/header/header.component';
import { MenuComponent } from './components/layout/menu/menu.component';
import { FooterComponent } from './components/layout/footer/footer.component';
import { MatIconModule } from '@angular/material/icon'
import { MatMenuModule } from '@angular/material/menu';
import { OpenLayerMapComponent } from './components/maps/open-layer-map/open-layer-map.component';
import { AddressFormComponent } from './components/shared/address-form/address-form.component';
import { ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { LoginComponent } from './components/login/login.component';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { SignupComponent } from './components/signup/signup.component';
import { AddresssesComponent } from './components/addressses/addressses.component';

@NgModule({
  declarations: [
    AppComponent,
    MapContainerComponent,
    HeaderComponent,
    MenuComponent,
    FooterComponent,
    OpenLayerMapComponent,
    AddressFormComponent,
    LoginComponent,
    SignupComponent,
    AddresssesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatIconModule,
    MatMenuModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [
    {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
