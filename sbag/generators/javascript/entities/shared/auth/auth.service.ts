import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  login(data: any) {
		return this.http.post<any>(environment.api + '/auth/login', data);
	}

  getToken(){
    let token = localStorage.getItem('User-token');
		return token == null ? '' : 'Bearer ' + token;
  }
}
