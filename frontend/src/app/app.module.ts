import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

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

@NgModule({
  declarations: [
    AppComponent,
    MapContainerComponent,
    HeaderComponent,
    MenuComponent,
    FooterComponent,
    OpenLayerMapComponent,
    AddressFormComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatIconModule,
    MatMenuModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
