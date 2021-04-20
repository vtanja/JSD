import {Component, OnInit} from '@angular/core';
import {FormBuilder} from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router'; 
import { SharedService} from '../../shared.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

    loginForm: any;

    constructor(private formBuilder: FormBuilder,
            private authService: AuthService,
            private router: Router,
            private sharedService: SharedService) 
    {}


    ngOnInit(): void {
      this.sharedService.isLoading(false);
      this.loginForm = this.formBuilder.group({
        username: '',
        password: '',
      });
    }

    
    onSubmit(value: Object) {
      this.sharedService.isLoading(false);

      this.authService.login(value).subscribe(
        (data) => {
          localStorage.setItem('User-token', data.accessToken);
          localStorage.setItem('Expires-in', data.expiresIn);
          localStorage.setItem('Refresh-token', data.refreshToken);
          localStorage.setItem('Username', data.username);
          localStorage.setItem('User-role', data.role);
          this.loginForm.reset();

          this.sharedService.isLogged(true);
          this.router.navigate(['']);
        },
        (error) => {
          if(error.status === 401){
            alert("Wrong username or password");
          }
          else {
            alert(error.error);
          }
        }
      );
    }
}
