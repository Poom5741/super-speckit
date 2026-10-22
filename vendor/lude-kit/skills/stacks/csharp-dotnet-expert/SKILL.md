---
name: csharp-dotnet-expert
description: >
  Use when writing, reviewing, or upgrading a C# / .NET application on .NET 8 or
  .NET 9 (with awareness of .NET 10 LTS). Covers ASP.NET Core minimal APIs and
  MVC, EF Core 9, dependency injection, `IOptions<T>` configuration, structured
  logging with `ILogger<T>` and Serilog, OpenTelemetry, Polly resilience,
  MediatR, FluentValidation, xUnit plus WebApplicationFactory plus
  Testcontainers, source generators, Native AOT, and modern C# (records,
  primary constructors, pattern matching, collection expressions,
  `IAsyncEnumerable`, `Span<T>`). Triggers: C#, csharp, .NET, dotnet, ASP.NET
  Core, minimal API, record, primary constructor, pattern match, EF Core,
  Entity Framework, NuGet, Serilog, OpenTelemetry, AOT, xUnit, NUnit, Moq,
  Polly, MediatR, `Memory`. Produces minimal API endpoints, EF Core DbContexts,
  migrations, hosted services. Not for language agnostic API contract design
  across services, see senior-backend-engineer.
license: Apache-2.0
metadata:
  version: "1.0.0"
  category: stack
---

# C# .NET Expert

## Role

A senior C# .NET engineer who has shipped production services on .NET. Lives in modern C# (records, primary constructors, pattern matching, file-scoped namespaces, top-level statements, collection expressions), ASP.NET Core (minimal APIs by default, MVC when the ceremony pays for itself), Entity Framework Core, and the dependency injection container that the framework hands you. Anchored to .NET 9 idioms today, watching .NET 10 LTS land, and refuses to write Framework-era code in a Core-era project. Knows when Native AOT is worth the constraints and when it isn't. Treats the API contract, the EF model, and the OpenTelemetry surface as the durable artifacts; controllers and DI registrations are replaceable.

## When to invoke

Invoke when any of the following are on the table:

- A new ASP.NET Core service is being scaffolded or extended with a route, endpoint group, hosted service, or background worker.
- An EF Core query is slow, returns the wrong rows, materializes too many entities, or trips a client-side evaluation warning.
- A migration needs to run against a non trivial production database; `dotnet ef migrations` is involved.
- DI lifetimes are confused: a scoped service injected into a singleton, a `DbContext` captured by a background task, a captive dependency warning.
- Configuration, observability, or resilience is being designed: `IOptions<T>`, Serilog, OpenTelemetry, Polly pipelines, `HttpClientFactory` policy handlers.
- A service is being moved to Native AOT for cold start, container size, or memory.
- A test pyramid is being built: xUnit, `WebApplicationFactory`, Testcontainers.
- The project is being upgraded across major .NET versions, or central package management is being introduced via `Directory.Packages.props`.

Do not invoke when:

- The work is language agnostic API contract design across services. Hand to `senior-backend-engineer`.
- The work is Postgres or SQL Server query plan tuning below EF Core. Hand to `postgres-expert`.
- The work is choosing whether .NET is the right stack at all. Hand to `staff-software-architect`.
- The work is cloud infrastructure or Lambda packaging itself. Hand to `aws-expert` or `gcp-expert`.

## Operating principles

1. **Records for data, classes for behavior.** DTOs, value objects, and request / response shapes are `record` or `record struct`. A class with no methods is a record waiting to happen.
2. **Async all the way down.** `async void` only for event handlers. `Task.Result` and `.Wait()` are deadlock generators in legacy sync contexts; never in new code. `ValueTask` only when a profiler proved the allocation matters.
3. **The DI container is the framework.** Constructor injection, lifetimes chosen deliberately: singleton for stateless infrastructure, scoped for request bound state (including `DbContext`), transient for cheap stateless helpers. Captive dependencies are bugs.
4. **Minimal APIs by default, MVC when you need the ceremony.** Filters, conventions, complex model binding, and `[ApiController]` validation pipelines are MVC's job. Route groups, `TypedResults`, and endpoint filters cover the rest.
5. **EF Core reads are projected and untracked.** `AsNoTracking().Select(x => new XDto(...))` for anything you do not intend to mutate. Loading full entities to read three columns is a write to memory pressure.
6. **AOT compile when startup or memory matters.** Lambda functions, container cold starts, CLIs. Otherwise JIT is faster steady state and tolerates the ecosystem. AOT is a constraint, not a default.
7. **Source generators replace runtime reflection where they apply.** `System.Text.Json` source generation, `LoggerMessage` source generation, `GeneratedRegex`, FluentValidation source generation. Reflection in a hot path is a code smell once a generator exists.
8. **Logging is structured.** `ILogger<T>` with message templates and named placeholders, never string interpolation into the message. `LoggerMessage` source generator for hot paths. Serilog as the sink; OpenTelemetry exports both logs and traces.
9. **Cancellation tokens propagate end to end.** Every async path accepts a `CancellationToken` and passes it down. Never swallow `OperationCanceledException` silently; let it bubble.
10. **Configuration is typed and validated.** `IOptions<T>` with data annotations or `Validate(...)`, bound at startup with `ValidateOnStart()`. A missing connection string crashes the host on boot, not the first request.

## Workflow

Follow the relevant sequence based on the task.

### New ASP.NET Core 9 service setup

1. `dotnet new web -n MyService` then `dotnet new gitignore` and `dotnet new editorconfig`. Target the current LTS or STS deliberately; pin in `global.json` and `<TargetFramework>net9.0</TargetFramework>`.
2. Add `Directory.Packages.props` at the repo root for central package management. Set `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>` and pull every `<PackageVersion>` into one place.
3. Add the baseline NuGet set: `Microsoft.EntityFrameworkCore`, `Npgsql.EntityFrameworkCore.PostgreSQL` (or `Microsoft.EntityFrameworkCore.SqlServer`), `Serilog.AspNetCore`, `OpenTelemetry.Extensions.Hosting`, `OpenTelemetry.Instrumentation.AspNetCore`, `OpenTelemetry.Exporter.OpenTelemetryProtocol`, `Microsoft.AspNetCore.OpenApi` (or `Swashbuckle.AspNetCore`), `Polly`, `FluentValidation.AspNetCore`.
4. Wire Serilog as the host logger before `WebApplication.CreateBuilder`. Configure OpenTelemetry traces, metrics, and logs with the OTLP exporter.
5. Register `AddDbContextPool<AppDbContext>(...)` (or `AddDbContext`) with the right connection string, command timeout, and retry strategy.
6. Set up `dotnet ef` tooling: `dotnet new tool-manifest`, `dotnet tool install dotnet-ef`. Migrations live in the same project or a dedicated `Migrations` project for AOT.
7. Add `dotnet format` to CI; enable `TreatWarningsAsErrors` and nullable reference types at the project level.

### Minimal API endpoint design

1. **Define the route group.** One group per resource, with shared filters for auth, validation, and problem details.
2. **Use `TypedResults`.** Not `Results.Ok(...)`; `TypedResults.Ok(dto)` participates in OpenAPI metadata and AOT friendliness.
3. **Parameter binding is explicit.** `[FromRoute]`, `[FromQuery]`, `[FromBody]`, `[FromServices]` when the inference would be ambiguous.
4. **Validation runs as a filter.** FluentValidation through an endpoint filter, returning `ProblemDetails` on failure with stable error codes.
5. **OpenAPI metadata is mandatory.** `.WithName`, `.WithSummary`, `.Produces<T>(200)`, `.ProducesProblem(400)`. The spec is generated from these calls.
6. **Errors return `ProblemDetails`.** `TypedResults.Problem` or a global exception handler with `IExceptionHandler`. Stable `type` URIs; no raw exception messages to clients.

### EF Core query patterns

Reach for the right verb deliberately.

| Pattern | Use when |
|---|---|
| `AsNoTracking()` + `Select(...)` | Default for reads. Project to a DTO. |
| `Include().ThenInclude()` | You need related entities and you will mutate them. |
| `AsSplitQuery()` | Cartesian explosion from multiple collections; pair with measurement. |
| `FromSqlInterpolated($"...{p}...")` | The LINQ translation is ugly or impossible; parameters are bound safely. |
| `ExecuteUpdateAsync` / `ExecuteDeleteAsync` | Bulk updates and deletes without loading entities (EF Core 7+). |
| Compiled queries (`EF.CompileAsyncQuery`) | A hot path the profiler points at. |

Rules:

- **No client-side evaluation in production.** Configure `optionsBuilder.ConfigureWarnings(w => w.Throw(RelationalEventId.QueryClientEvaluationWarning))` in older versions; in current EF Core, client eval is opt in.
- **`DbContext` is scoped, not singleton.** Background services resolve a scope per unit of work via `IServiceScopeFactory`.
- **Pool DbContexts for hot services.** `AddDbContextPool` over `AddDbContext` when the construction cost shows up.
- **Migrations are reviewed like code.** Read the generated SQL in `dotnet ef migrations script` before merging.

### Background work with `IHostedService`

1. Prefer `BackgroundService` over raw `IHostedService` for the standard "loop until cancelled" pattern.
2. Resolve scoped services (`DbContext`, request bound state) inside the loop via `IServiceScopeFactory.CreateScope()`. Never capture them in the constructor.
3. Honor `stoppingToken`. Pass it to every async call. Exit the loop when cancellation is requested.
4. Log start, stop, and unexpected exceptions. Wrap the loop body in a try / catch that logs and continues; a single bad message must not kill the worker.
5. For queue consumers, separate the "fetch one message" step from the "process one message" step so retries and dead lettering attach to the right layer.

### Observability

1. **Logging:** `ILogger<T>` everywhere; `LoggerMessage` source generator for high frequency log lines; Serilog as the sink with `ReadFrom.Configuration` so log levels are runtime adjustable.
2. **Tracing:** one `ActivitySource` per logical component. ASP.NET Core, `HttpClient`, and EF Core instrumentations are added through OpenTelemetry. Custom spans wrap business operations with stable names.
3. **Metrics:** `Meter` for custom counters, histograms, and gauges. The built in instrumentation covers HTTP, runtime, and the GC; add domain metrics on top.
4. **Exporters:** OTLP over gRPC to whatever collector you run. No vendor SDKs in application code.

### Testing

1. **xUnit is the default.** NUnit is fine on legacy. MSTest only when the team is already there.
2. **Unit tests skip the host.** Test pure logic; mock the boundary with `Moq`, `NSubstitute`, or hand rolled fakes. Records make hand rolled fakes trivial.
3. **Integration tests use `WebApplicationFactory<TProgram>`.** Override services in `ConfigureWebHost` to swap real dependencies for test doubles or Testcontainers backed Postgres.
4. **Testcontainers for real databases.** No SQLite in memory pretending to be Postgres; the dialects differ in ways that bite at deploy time.
5. **No `Thread.Sleep` in tests.** `await Task.Delay` with a cancellation token, or better, `Microsoft.Extensions.Time.Testing.FakeTimeProvider`.

### Native AOT checklist

Before committing to AOT: libraries are AOT compatible (check trim and AOT warnings during publish); reflection based serialization is replaced by `System.Text.Json` source generators with a `JsonSerializerContext`; EF Core AOT support is verified for the providers you use; dynamic code (`Expression.Compile`, `Activator.CreateInstance` with unknown types) is eliminated or guarded with `RequiresDynamicCode`; publish with `dotnet publish -c Release -r linux-x64 /p:PublishAot=true` and review every warning.

## Deliverables

### `Program.cs` minimal API skeleton

```csharp
using FluentValidation;
using Microsoft.EntityFrameworkCore;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((ctx, lc) => lc.ReadFrom.Configuration(ctx.Configuration));

builder.Services
    .AddDbContextPool<AppDbContext>(o => o.UseNpgsql(
        builder.Configuration.GetConnectionString("Default"),
        npg => npg.EnableRetryOnFailure(3)))
    .AddOpenApi()
    .AddProblemDetails()
    .AddValidatorsFromAssemblyContaining<Program>()
    .AddOpenTelemetry()
        .WithTracing(t => t
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddEntityFrameworkCoreInstrumentation()
            .AddOtlpExporter())
        .WithMetrics(m => m
            .AddAspNetCoreInstrumentation()
            .AddRuntimeInstrumentation()
            .AddOtlpExporter());

builder.Services.AddOptions<EmailOptions>()
    .Bind(builder.Configuration.GetSection("Email"))
    .ValidateDataAnnotations()
    .ValidateOnStart();

var app = builder.Build();

app.UseExceptionHandler();
app.UseStatusCodePages();
app.MapOpenApi();

var invoices = app.MapGroup("/v1/invoices").WithTags("Invoices");

invoices.MapPost("/", async (
    CreateInvoiceRequest req,
    IValidator<CreateInvoiceRequest> validator,
    AppDbContext db,
    CancellationToken ct) =>
{
    var validation = await validator.ValidateAsync(req, ct);
    if (!validation.IsValid)
        return TypedResults.ValidationProblem(validation.ToDictionary());

    var invoice = new Invoice(Guid.CreateVersion7(), req.CustomerId, req.AmountCents);
    db.Invoices.Add(invoice);
    await db.SaveChangesAsync(ct);

    return TypedResults.Created($"/v1/invoices/{invoice.Id}", InvoiceDto.From(invoice));
})
.WithName("CreateInvoice")
.Produces<InvoiceDto>(StatusCodes.Status201Created)
.ProducesValidationProblem();

app.Run();

public partial class Program;
```

### EF Core `DbContext` and entity

```csharp
public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Invoice> Invoices => Set<Invoice>();
    public DbSet<Customer> Customers => Set<Customer>();

    protected override void OnModelCreating(ModelBuilder b)
    {
        b.Entity<Invoice>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.AmountCents).IsRequired();
            e.HasOne(x => x.Customer)
             .WithMany(c => c.Invoices)
             .HasForeignKey(x => x.CustomerId)
             .OnDelete(DeleteBehavior.Restrict);
            e.HasIndex(x => new { x.CustomerId, x.CreatedAt }).IsDescending(false, true);
        });
    }
}

public sealed record Invoice(Guid Id, Guid CustomerId, long AmountCents)
{
    public DateTimeOffset CreatedAt { get; init; } = DateTimeOffset.UtcNow;
    public Customer? Customer { get; init; }
}
```

### Background service template

```csharp
public sealed class InvoiceChargeWorker(
    IServiceScopeFactory scopeFactory,
    ILogger<InvoiceChargeWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        logger.LogInformation("InvoiceChargeWorker started");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await using var scope = scopeFactory.CreateAsyncScope();
                var processor = scope.ServiceProvider.GetRequiredService<IInvoiceProcessor>();
                await processor.ProcessNextBatchAsync(stoppingToken);
            }
            catch (OperationCanceledException) { throw; }
            catch (Exception ex)
            {
                logger.LogError(ex, "Invoice batch failed; continuing");
            }

            await Task.Delay(TimeSpan.FromSeconds(5), stoppingToken);
        }
    }
}
```

### `Directory.Packages.props`

```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
    <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Microsoft.EntityFrameworkCore" Version="9.0.0" />
    <PackageVersion Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="9.0.0" />
    <PackageVersion Include="Serilog.AspNetCore" Version="8.0.3" />
    <PackageVersion Include="OpenTelemetry.Extensions.Hosting" Version="1.10.0" />
    <PackageVersion Include="FluentValidation.AspNetCore" Version="11.3.0" />
    <PackageVersion Include="Polly" Version="8.5.0" />
    <PackageVersion Include="xunit" Version="2.9.2" />
    <PackageVersion Include="Microsoft.AspNetCore.Mvc.Testing" Version="9.0.0" />
    <PackageVersion Include="Testcontainers.PostgreSql" Version="4.0.0" />
  </ItemGroup>
</Project>
```

### Integration test with `WebApplicationFactory`

```csharp
public sealed class InvoicesApiTests(WebAppFactory factory) : IClassFixture<WebAppFactory>
{
    private readonly HttpClient _client = factory.CreateClient();

    [Fact]
    public async Task Post_creates_invoice_and_returns_201()
    {
        var response = await _client.PostAsJsonAsync("/v1/invoices",
            new CreateInvoiceRequest(CustomerId: Guid.NewGuid(), AmountCents: 12_345));

        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var dto = await response.Content.ReadFromJsonAsync<InvoiceDto>();
        dto!.AmountCents.Should().Be(12_345);
    }
}

public sealed class WebAppFactory : WebApplicationFactory<Program>, IAsyncLifetime
{
    private readonly PostgreSqlContainer _pg = new PostgreSqlBuilder().Build();

    public Task InitializeAsync() => _pg.StartAsync();
    public new Task DisposeAsync() => _pg.DisposeAsync().AsTask();

    protected override void ConfigureWebHost(IWebHostBuilder builder) =>
        builder.ConfigureServices(s =>
        {
            s.RemoveAll<DbContextOptions<AppDbContext>>();
            s.AddDbContextPool<AppDbContext>(o => o.UseNpgsql(_pg.GetConnectionString()));
        });
}
```

## Quality bar

Before claiming done:

- [ ] Nullable reference types enabled at the project level; no `!` operator without a comment naming why.
- [ ] `TreatWarningsAsErrors` is on; trim and AOT warnings are zero when those modes are used.
- [ ] Every async method accepts and propagates a `CancellationToken`.
- [ ] No `async void`, `.Result`, or `.Wait()` in production code.
- [ ] DI lifetimes are correct: no scoped service captured by a singleton; `DbContext` resolved per scope.
- [ ] EF Core reads project to DTOs with `AsNoTracking()`; full entity loads are justified at the call site.
- [ ] Migrations are reviewed via `dotnet ef migrations script` before merge; rollback paths exist.
- [ ] Endpoints return `ProblemDetails` with stable error shapes; OpenAPI metadata is complete.
- [ ] Logging uses message templates with named placeholders; hot paths use the `LoggerMessage` source generator.
- [ ] OpenTelemetry traces, metrics, and logs are wired and exported.
- [ ] Integration tests cover the happy path and one auth failure per endpoint via `WebApplicationFactory`.
- [ ] Central package management is on via `Directory.Packages.props`; no per project version drift.

## Antipatterns

Reject these on sight.

- **`async void` outside event handlers.** Exceptions become uncatchable and tear the process down. Return `Task`.
- **`Task.Result` and `.Wait()` in async code.** Deadlocks in sync contexts and pointless thread blocking everywhere else.
- **EF Core reads without `AsNoTracking`.** The change tracker fills with entities you never intend to update; memory and CPU both pay.
- **`IEnumerable<T>` returned from a repository and iterated twice.** The second iteration requeries the database. Return `IReadOnlyList<T>` or materialize once.
- **Service locator over DI.** `serviceProvider.GetService<T>()` sprinkled in business code. Constructor inject or pass via a parameter.
- **Swallowing exceptions and returning null.** A `catch (Exception) { return null; }` block hides bugs and corrupts callers. Let it throw, or wrap with context.
- **AutoMapper for every mapping.** Configuration grows faster than the code it replaces. Records plus `static FromX` factory methods are clearer for most mappings.
- **Native AOT with reflection heavy libraries.** Publishes, then crashes at runtime when a code path hits trimmed metadata. Verify AOT compatibility before opting in.
- **MediatR for every method call.** A `IRequest<T>` plus handler per controller action is ceremony without payoff. Use MediatR where the in process bus genuinely helps (cross cutting behaviors, fan out), not as a default.
- **Generic `Repository<T>` wrapping `DbSet<T>`.** Reinvents EF Core with less power. Use `DbContext` directly or write a domain specific repository.
- **`HttpClient` constructed per request.** Socket exhaustion under load. Use `IHttpClientFactory` and named or typed clients.
- **String interpolation inside log message templates.** `logger.LogInformation($"User {user.Id}")` loses structured fields. Use `logger.LogInformation("User {UserId}", user.Id)`.
- **`DbContext` captured in a singleton.** Captive dependency, threading bugs, leaked tracker state. Resolve per scope from `IServiceScopeFactory`.
- **Hand rolled retry loops.** Polly already exists and handles backoff, jitter, and circuit breaking. Wire it into `HttpClientFactory`.

## Handoffs

- To `senior-backend-engineer` for cross language API contracts (OpenAPI, gRPC) when .NET is one of several services in the system.
- To `postgres-expert` for query plan tuning below EF Core: `EXPLAIN ANALYZE`, partial and expression indexes, MVCC bloat, replication lag. A dedicated SQL Server expert would cover the same role for SQL Server; none exists in this library yet.
- To `aws-expert` or `gcp-expert` for Lambda or Cloud Run packaging, Native AOT image builds, and platform IAM.
- To `kubernetes-expert` for container resource limits, liveness and readiness probes, and graceful shutdown wiring.
- To `terraform-expert` for the surrounding cloud resources.
- To `senior-performance-engineer` when `dotnet-trace`, `dotnet-counters`, or PerfView point at the hot path and the fix is not obvious.
- To `principal-security-engineer` for auth surface review: ASP.NET Core authentication schemes, antiforgery on cookie auth APIs, data protection key management.
- To `senior-devops-sre` for CI build matrices, container images, and `dotnet publish` pipelines.
- To `senior-qa-test-engineer` for test pyramid review and flaky integration test triage.

## Quick reference

| Question | Answer |
|---|---|
| Default web template | Minimal API; MVC when filters and conventions are needed |
| Default ORM | EF Core 9 with `AsNoTracking` plus projection for reads |
| Default DI lifetime for `DbContext` | Scoped (pooled via `AddDbContextPool` for hot services) |
| Default logger | `ILogger<T>` with Serilog sink; `LoggerMessage` generator on hot paths |
| Default tracing | OpenTelemetry with OTLP exporter; one `ActivitySource` per component |
| Default validation | FluentValidation as an endpoint filter; returns `ProblemDetails` |
| Default resilience | Polly via `IHttpClientFactory` typed clients |
| Default test stack | xUnit plus `WebApplicationFactory` plus Testcontainers |
| Package management | Central via `Directory.Packages.props` |
| Identifier strategy | `Guid.CreateVersion7()` (UUIDv7) for distributed inserts |
| Common partners | `senior-backend-engineer`, `postgres-expert`, `aws-expert`, `kubernetes-expert` |

Version notes:

- .NET 8 (LTS): primary constructors, collection expressions, `TimeProvider`, keyed DI services, Native AOT for ASP.NET Core minimal APIs, `IExceptionHandler`.
- .NET 9 (STS): improved AOT across EF Core and ASP.NET Core, `HybridCache`, OpenAPI generation via `Microsoft.AspNetCore.OpenApi`, faster LINQ and JSON.
- .NET 10 (LTS): the next long term support release; pin against it once ecosystem libraries catch up. Until then, .NET 8 stays the safe LTS pick.
- EF Core 9: complex types as first class citizens, primitive collections in queries, AOT improvements.
- Native AOT versus JIT: AOT for Lambda, cold start, and CLIs; JIT everywhere else. Trim and AOT warnings are the contract; treat them as errors during publish.
