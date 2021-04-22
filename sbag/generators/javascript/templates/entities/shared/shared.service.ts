import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  isLoadingSubject: Subject<boolean> = new Subject<boolean>();

  loggedInSubject: Subject<boolean> = new Subject<boolean>();

  constructor() { }

  isLoading(loading: boolean) {
    this.isLoadingSubject.next(loading);
  }

  isLogged(logged: boolean){
    this.loggedInSubject.next(logged);
  }

}
