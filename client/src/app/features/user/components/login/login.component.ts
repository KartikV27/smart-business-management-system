import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../../service/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  loginForm: FormGroup;
  registerForm: FormGroup;
  errorMessage: string = '';
  isRegisterMode: boolean = false;
  successMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });

    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      role: ['USER']
    });
  }

  toggleMode() {
    this.isRegisterMode = !this.isRegisterMode;
    this.errorMessage = '';
    this.successMessage = '';
  }

  onSubmit() {
    if (this.isRegisterMode) {
      if (this.registerForm.valid) {
        this.userService.register(this.registerForm.value).subscribe({
          next: (res) => {
            this.successMessage = 'Registration successful! You can now log in.';
            this.isRegisterMode = false; // switch back to login
            this.registerForm.reset({role: 'USER'});
          },
          error: (err) => {
            this.errorMessage = err.error?.detail || 'Registration failed';
          }
        });
      }
    } else {
      if (this.loginForm.valid) {
        this.userService.login(this.loginForm.value).subscribe({
          next: (res) => {
            this.router.navigate(['/dashboard']);
          },
          error: (err) => {
            this.errorMessage = err.error?.detail || 'Invalid credentials';
          }
        });
      }
    }
  }

  setupDatabase() {
    this.userService.setupAdmin().subscribe({
      next: (res) => alert(res.message),
      error: (err) => alert(err.error?.detail || 'Setup failed')
    });
  }
}
