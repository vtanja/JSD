import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoaderComponent } from './loader/loader.component';
import { HeaderComponent } from './header/header.component';
import { HomepageComponent } from './homepage/homepage.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './../app-routing.module'


@NgModule({
  declarations: [LoaderComponent, HeaderComponent, HomepageComponent],
  imports: [
    CommonModule,
    NgbModule,
    AppRoutingModule
  ],
  exports: [
    LoaderComponent,
    HeaderComponent,
    HomepageComponent
  ]
})
export class SharedModule { }
