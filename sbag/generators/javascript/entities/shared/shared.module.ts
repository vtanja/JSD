import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoaderComponent } from './loader/loader.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { HomepageComponent } from './homepage/homepage.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './../app-routing.module'


@NgModule({
  declarations: [LoaderComponent, HeaderComponent, HomepageComponent, FooterComponent],
  imports: [
    CommonModule,
    NgbModule,
    AppRoutingModule
  ],
  exports: [
    LoaderComponent,
    HeaderComponent,
    HomepageComponent,
    FooterComponent
  ]
})
export class SharedModule { }
