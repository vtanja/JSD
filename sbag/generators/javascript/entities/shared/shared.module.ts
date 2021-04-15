import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoaderComponent } from './loader/loader.component';
import { HeaderComponent } from './header/header.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './../app-routing.module'


@NgModule({
  declarations: [LoaderComponent, HeaderComponent],
  imports: [
    CommonModule,
    NgbModule,
    AppRoutingModule
  ],
  exports: [
    LoaderComponent,
    HeaderComponent
  ]
})
export class SharedModule { }
