import { Component, OnInit, Input } from '@angular/core';
import { SharedService } from '../shared.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  @Input() isLogged = false;

  constructor(private sharedService: SharedService, private router: Router) { }

  ngOnInit() { 
    
  }

  logout(){
    localStorage.clear();
    this.sharedService.isLogged(false);
    this.router.navigateByUrl('/login', { skipLocationChange: true }).then(() => {
      this.router.navigate(['']);
  });
  }
}
