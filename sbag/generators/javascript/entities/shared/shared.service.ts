import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  isLoadingSubject: Subject<boolean> = new Subject<boolean>();

  constructor() { }

  isLoading(loading: boolean) {
    this.isLoadingSubject.next(loading);
  }

}
