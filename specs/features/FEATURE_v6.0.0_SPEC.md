# Strategic Operations Specification: Release v6.0.0 Enterprise Multi-Tenant SaaS

**Document Owner**: CEO & Chief Architect
**Status**: APPROVED FOR IMPLEMENTATION 🟢

## 1. Problem Statement
The current system assumes a single underlying hospital/clinic group logic. To commercialize the platform, we need true multi-tenant isolation where completely unrelated clinics can sign up, pay a subscription, and use the platform securely.

## 2. Solution Overview
Introduce a `Tenant` entity at the root of the domain. Map `ClinicEntity` and `User` to `TenantId`. Implement Global Query Filters in EF Core.

## 3. Business Rules
- **`BR-SAAS-01` (Tenant Isolation)**: All database queries must automatically filter by the authenticated user's `TenantId`.
- **`BR-SAAS-02` (Custom Subdomains)**: Users logging into a tenant subdomain (e.g., `dr-smith.cliniccorp.ai`) will automatically resolve the `TenantId`.
- **`BR-SAAS-03` (Tiered Access)**: Subscription tiers (Starter, Pro, Enterprise) limit active doctors and storage capacity.
