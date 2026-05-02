import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'ML Dashboard';
  menuOpen = false;

  constructor(private router: Router) { }

  toggleMenu(): void {
    this.menuOpen = !this.menuOpen;
  }

  navigate(path: string): void {
    this.router.navigate([path]);
    this.menuOpen = false;
  }

  isActive(path: string): boolean {
    return this.router.url === path;
  }
}
