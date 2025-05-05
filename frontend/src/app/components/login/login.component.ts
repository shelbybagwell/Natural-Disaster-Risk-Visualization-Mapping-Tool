import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})

export class LoginComponent {

  loginForm!: FormGroup;
  http = inject(HttpClient);
  loginUrl = 'http://localhost:5000/auth/login';

  constructor(private fb: FormBuilder, private router: Router) {
    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  login() { 

    //Clear access token
    localStorage.setItem('access_token', "");

    if (!this.loginForm.valid) {
      alert('Please fill in all required fields.');
      return;
    } 
      
    const { email, password } = this.loginForm.value;

    this.http.post<any[]>(this.loginUrl, { email, password }).subscribe({
      next: (response: any) => {

        console.log(response);

        localStorage.setItem('access_token', response.access_token);
        this.router.navigate(['/map']);
      },
      error: (data) => {
        console.log(data.error?.error);
        alert(data.error?.error);
      }, 
    });
  }

  signUp(){
    this.router.navigate(['/signUp'])
  }
}