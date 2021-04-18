import { Component } from '@angular/core';
import { SharedService } from 'src/app/shared/shared.service';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent{

  constructor(
    private sharedService: SharedService
  ) { 
    this.sharedService.isLoading(false);
  }
}
