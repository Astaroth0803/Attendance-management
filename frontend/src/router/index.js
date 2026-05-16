import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import SuperAdminLayout from '../layouts/SuperAdminLayout.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/HomeView.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/LoginView.vue')
    },
    {
        path: '/attendance',
        name: 'Attendance',
        component: () => import('../views/AttendanceFormView.vue')
    },
    {
        path: '/super-admin',
        component: SuperAdminLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                name: 'SuperAdminDashboard',
                component: () => import('../views/superadmin/SuperAdminDashboard.vue')
            }
        ]
    },
    // Authenticated routes — rendered inside AppLayout (sidebar)
    {
        path: '/',
        component: AppLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: () => import('../views/DashboardView.vue')
            },
            {
                path: 'beneficiaries',
                name: 'Beneficiaries',
                component: () => import('../views/BeneficiariesView.vue')
            },
            {
                path: 'activities',
                name: 'Activities',
                component: () => import('../views/ActivitiesView.vue')
            },
            {
                path: 'reports',
                name: 'Reports',
                component: () => import('../views/ReportsView.vue')
            },
            {
                path: 'beneficiaries/:id',
                name: 'BeneficiaryProfile',
                component: () => import('../views/BeneficiaryProfileView.vue')
            },
            {
                path: 'activities/:id',
                name: 'ActivityProfile',
                component: () => import('../views/ActivityProfileView.vue')
            },
            {
                path: 'admins',
                name: 'Admins',
                component: () => import('../views/AdminsView.vue')
            },
            {
                path: 'excursions',
                name: 'Excursions',
                component: () => import('../views/ExcursionsView.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const isAuth = !!localStorage.getItem('access_token');

    if (to.meta.requiresAuth && !isAuth) {
        next('/login');
    } else if (to.path === '/login' && isAuth) {
        next('/dashboard');
    } else {
        next();
    }
});

export default router
