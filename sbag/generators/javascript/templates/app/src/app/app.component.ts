import { Component, OnInit } from '@angular/core';
import { SharedService } from './shared/shared.service';
import { AuthService } from './shared/auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    title = 'app';
    isLoading: boolean = true;
    isLogged: boolean = false;

    constructor(private sharedService: SharedService, private authService: AuthService){
      this.isLogged = this.authService.getToken() != '' ? true: false;
    }

    ngOnInit() {
      this.sharedService.isLoadingSubject.subscribe((res : any) => {
        this.isLoading = res;
      });

      this.sharedService.loggedInSubject.subscribe((res: any) => {
        this.isLogged = res;
      });
    }
}
