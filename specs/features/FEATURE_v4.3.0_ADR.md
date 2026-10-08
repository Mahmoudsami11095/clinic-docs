# Architecture Decision Record (ADR): Inter-Branch Stock Transfers & Logistics State Machine (Release v4.3.0)

**Document Owner**: Chief Architect & Technical Lead Agent (`chief_architect`)  
**Status**: APPROVED  
**Date**: 2026-10-08  
**Scope**: `ClinicApi` (Domain, Application, Infrastructure, API) & `clinic-app` (Inventory Module)  

---

## 1. Context & Architectural Problem

As the clinic ecosystem expands to multiple operating branches and regional hubs, medical inventory must move between physical facilities. A naive approach (direct synchronous updates across clinic inventory records) introduces severe risks:
1. **Phantom Inventory**: If stock is deducted at Clinic A but not immediately received at Clinic B, goods in transit disappear from valuations.
2. **Double Consumption**: If stock remains visible at Clinic A while in transit, another doctor at Clinic A may consume it for a procedure before the courier collects it.
3. **Audit Loss**: Untracked inter-clinic shipments violate medical device traceability regulations (ISO 13485 & Egyptian Drug Authority).

## 2. Decision: Two-Phase Event-Driven Transfer State Machine

We adopt a **Two-Phase Commit Transfer State Machine** with transactional isolation and real-time SignalR notifications:

### 2.1 Domain Model (`Clinic.Domain`)
```csharp
public class StockTransferRequisition
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string RequisitionNumber { get; set; } = string.Empty; // e.g. TRF-202610-0012
    public string SourceClinicId { get; set; } = string.Empty;
    public ClinicEntity SourceClinic { get; set; } = null!;
    public string DestinationClinicId { get; set; } = string.Empty;
    public ClinicEntity DestinationClinic { get; set; } = null!;
    
    public string MaterialId { get; set; } = string.Empty;
    public Material Material { get; set; } = null!;
    
    public int QuantityRequested { get; set; }
    public int? QuantityDispatched { get; set; }
    public int? QuantityReceived { get; set; }
    public int QuantityDamaged { get; set; } = 0;
    
    public string? BatchNumber { get; set; }
    public DateTime? ExpiryDate { get; set; }
    
    public string Priority { get; set; } = "Normal"; // "Normal", "Urgent", "Emergency"
    public string Status { get; set; } = "Requested"; // "Requested", "Approved", "InTransit", "Received", "Cancelled"
    
    public string RequestedByUserId { get; set; } = string.Empty;
    public string? DispatchedByUserId { get; set; }
    public string? ReceivedByUserId { get; set; }
    
    public DateTime RequestedAt { get; set; } = DateTime.UtcNow;
    public DateTime? DispatchedAt { get; set; }
    public DateTime? ReceivedAt { get; set; }
    public string? Notes { get; set; }
}
```

### 2.2 Concurrency & Transactional Guarantee
1. **Approval Phase**: Sets status to `Approved`. Flags `ReservedStock` on the source inventory line item without reducing physical count.
2. **Dispatch Phase (`BR-LOG-01`)**: Deducts physical count from the source clinic in an EF Core `IDbContextTransaction`. Transitions status to `InTransit`. Emits SignalR event `StockTransferDispatched`.
3. **Receiving Phase (`BR-LOG-02`)**: Adds physical count to the destination clinic within an isolated transaction. Logs damaged units to quarantine. Transitions status to `Received`. Emits SignalR event `StockTransferReceived`.

### 2.3 Real-Time SignalR Events
- `ReceiveStockTransferAlert`: Sent to clinic group `Clinic_{SourceClinicId}` upon creation.
- `ReceiveStockTransferInTransit`: Sent to clinic group `Clinic_{DestinationClinicId}` upon courier dispatch.
- `ReceiveStockTransferCompleted`: Broadcast to audit ledger.

---

## 3. Frontend Architecture (`clinic-app`)
- Standalone `StockTransferBoardComponent` integrated within `features/inventory/components/transfer-board/`.
- Signal-driven state: `outboundTransfers()`, `inboundTransfers()`, `pendingCount()`.
- Responsive inspection modal with damaged item counter and digital receiving signature.

---

## 4. Consequences
- **Positive**: Zero phantom inventory, rigorous traceability per ISO 13485, and immediate visibility for both source and destination clinical teams.
- **Trade-off**: Requires couriers or clinical staff to execute physical verification before destination stock is usable for procedures.
