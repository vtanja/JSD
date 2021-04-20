import { Component, OnInit } from '@angular/core';
import { SharedService } from './shared/shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    title = 'app';
    isLoading: boolean = true;

    constructor(private sharedService: SharedService){}

    ngOnInit() {
      this.sharedService.isLoadingSubject.subscribe((res : any) => {
        this.isLoading = res;
      });
    }
}
