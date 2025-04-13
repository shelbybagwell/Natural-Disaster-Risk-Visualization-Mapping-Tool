import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MapContainerComponent } from './components/maps/map-container/map-container.component';
import { OpenLayerMapComponent } from './components/maps/open-layer-map/open-layer-map.component';

@NgModule({
  declarations: [
    AppComponent,
    MapContainerComponent,
    OpenLayerMapComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
