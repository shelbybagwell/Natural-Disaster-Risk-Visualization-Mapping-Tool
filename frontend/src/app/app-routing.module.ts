import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MapContainerComponent } from './components/maps/map-container/map-container.component';
import {LoginComponent} from './components/login/login.component';

const routes: Routes = [
  {path: '', component: LoginComponent},
  {path: 'map', component: MapContainerComponent},
  {path:'**', redirectTo: ''}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
