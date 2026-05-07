import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'ML Dashboard';
  menuOpen = false;

  constructor(private router: Router) { }

  ngOnInit(): void {
    this.loadGoogleTranslate();
  }

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

  loadGoogleTranslate(): void {
    if (document.getElementById('google-translate-script')) {
      return;
    }

    (window as any).googleTranslateElementInit = () => {
      if (document.getElementById('google_translate_element')) {
        new (window as any).google.translate.TranslateElement(
          { pageLanguage: 'en', autoDisplay: false },
          'google_translate_element'
        );
      }
    };

    const script = document.createElement('script');
    script.id = 'google-translate-script';
    script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    script.async = true;
    document.body.appendChild(script);
  }
}
