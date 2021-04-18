import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoaderComponent } from './loader/loader.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { HomepageComponent } from './homepage/homepage.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './../app-routing.module';
import {LoginComponent} from './auth/login/login.component';
import {RegisterComponent} from './auth/register/register.component';
import {ReactiveFormsModule} from '@angular/forms';


@NgModule({
  declarations: [LoaderComponent, HeaderComponent, HomepageComponent, FooterComponent, LoginComponent,
  RegisterComponent],
  imports: [
    CommonModule,
    NgbModule,
    AppRoutingModule,
    ReactiveFormsModule
  ],
  exports: [
    LoaderComponent,
    HeaderComponent,
    HomepageComponent,
    FooterComponent,
    LoginComponent,
    RegisterComponent
  ]
})
export class SharedModule { }
