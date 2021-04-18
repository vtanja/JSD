import {Component, OnInit} from '@angular/core';
import {FormBuilder} from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

    loginForm: any;
    constructor(private formBuilder: FormBuilder) {}
    ngOnInit(): void {
      this.loginForm = this.formBuilder.group({
        email: '',
        password: '',
      });
    }
    onSubmit(value: object): void {}
}
