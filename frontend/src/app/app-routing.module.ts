import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MapContainerComponent } from './components/maps/map-container/map-container.component';

const routes: Routes = [
  {path: '', component: MapContainerComponent},
  {path: '*', component: MapContainerComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
