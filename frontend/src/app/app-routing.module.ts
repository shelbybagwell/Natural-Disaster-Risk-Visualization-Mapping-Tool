import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MapContainerComponent } from './components/maps/map-container/map-container.component';
import {LoginComponent} from './components/login/login.component';
import { SignupComponent } from './components/signup/signup.component';
import { AddresssesComponent } from './components/addressses/addressses.component';

const routes: Routes = [
  {path: '', component: LoginComponent},
  {path: 'map', component: MapContainerComponent},
  {path: 'signUp', component: SignupComponent},
  {path: 'addresses', component: AddresssesComponent},
  {path:'**', redirectTo: ''}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
