import { Component, OnInit } from '@angular/core';
import { SharedService } from 'src/app/shared/shared.service';
import { AuthService } from 'src/app/shared/auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit{

  constructor(
    private sharedService: SharedService,
    private authService: AuthService,
    private router: Router
  ) { 
    this.sharedService.isLoading(false);
  }

  ngOnInit(){
    if (this.authService.getToken() === '' || this.authService.getToken() === null || this.authService.getToken() === undefined){
        this.router.navigate(['login']);
    }
  }
}
