import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-signup',
  standalone: false,
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.scss'
})
export class SignupComponent {

  signUpForm!: FormGroup
  http = inject(HttpClient);
  signupUrl = 'http://localhost:5000/users/';

  constructor(private fb: FormBuilder, private router:Router){
    this.signUpForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required],
      confirm_password: ['', Validators.required]
    })
  }

  signUp() {

    if (!this.signUpForm.valid) {
      alert('Please fill in all required fields.');
      return;
    } 

    const { first_name, last_name, email, password, confirm_password } = this.signUpForm.value;
    
    //console.log(first_name, last_name, email, password, confirm_password);

    this.http.post<any[]>(this.signupUrl, { first_name, last_name, email, password, confirm_password }).subscribe({
      next: (response: any) => {

        console.log(response);

        this.router.navigate(['/']);
      },
      error: (data) => {
        console.log(data.error?.error);
        alert(data.error?.error);
      }, 
    });
  }
}
