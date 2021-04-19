import { Component, OnInit } from '@angular/core';
import {FormBuilder} from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

    registerForm: any;

    constructor(private formBuilder: FormBuilder, private authService: AuthService, private router: Router) {}

    ngOnInit(): void {
      this.registerForm = this.formBuilder.group({
        email: '',
        username: '',
        password: '',
      });
    }
    onSubmit(value: object): void {
      this.authService.register(value).subscribe((res:any) => {
          alert('You have registered successfully!');        
          this.router.navigate(['']);
      },
      (err)=>{
        console.log(err);
        alert('Unable to register! Try again!');     
        this.registerForm.reset();
      });
    }
}