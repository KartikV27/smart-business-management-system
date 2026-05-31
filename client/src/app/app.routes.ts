import { Routes } from '@angular/router';
import { LayoutComponent } from './core/layout/layout/layout.component';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { 
    path: 'login', 
    loadChildren: () => import('./features/user/user.module').then(m => m.UserModule)
  },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { 
        path: 'dashboard', 
        loadChildren: () => import('./features/dashboard/dashboard.module').then(m => m.DashboardModule) 
      },
      { 
        path: 'products', 
        loadChildren: () => import('./features/products/products.module').then(m => m.ProductsModule) 
      },
      { 
        path: 'billing', 
        loadChildren: () => import('./features/billing/billing.module').then(m => m.BillingModule) 
      },
      { 
        path: 'purchases', 
        loadChildren: () => import('./features/purchase/purchase.module').then(m => m.PurchaseModule) 
      }
    ]
  },
  { path: '**', redirectTo: '/dashboard' }
];
