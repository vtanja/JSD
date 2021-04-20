import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from 'src/app/shared/auth/auth.service';

@Injectable()
export class ApiPrefixInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const authToken = this.authService.getToken();

    if (authToken != '') {

			let authReq = request.clone({
				headers: request.headers.set('AuthToken', authToken),
			});

			return next.handle(authReq);

		} else {
			const req = request.clone({
				headers: request.headers.set('Content-Type', 'application/json'),
			});
			return next.handle(req);
		}
  }
}
