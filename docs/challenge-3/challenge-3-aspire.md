# Aspire - Challenge 3 - Pub/Sub
## Background information

For background information read: https://www.diagrid.io/blog/net-aspire-dapr-what-are-they-and-how-they-complement-each-other

## Prepare

Clone the repository: `https://github.com/kbr-ucl/dapr-workshop-csharp`

Checkout branch `challenge-3`

Create a new branch `aspire-challenge-3`


### Add  .NET Aspire Orchestration Support

- Right click `PizzaStorefront`project and add  `.NET Aspire Orchestration Support`

- Right click `PizzaKitchen`project and add  `.NET Aspire Orchestration Support`

- Right click `PizzaDelivery`project and add  `.NET Aspire Orchestration Support`

- Right click `PizzaOrder`project and add  `.NET Aspire Orchestration Support`



## Hosting integration

In your .NET Aspire solution, to integrate Dapr and access its types and APIs, add the [📦 Aspire.Hosting.Dapr](https://www.nuget.org/packages/Aspire.Hosting.Dapr) NuGet package in the `DaprWorkshop.AppHost` project.

```powershell
dotnet add package Aspire.Hosting.Dapr
```

### Nuget update

Use Nuget Packet Manager for solution to update packets.

### In folder DaprWorkshop.AppHost add changes to `Program.cs`

#### Add Dapr State Store to .NET Aspire resources
```c#
using Aspire.Hosting.Dapr;
using Projects;

var builder = DistributedApplication.CreateBuilder(args);

var statestore = builder.AddDaprStateStore("pizzastatestore");
```


#### Add Dapr SubSub to .NET Aspire resources

```c#
using Aspire.Hosting.Dapr;

var builder = DistributedApplication.CreateBuilder(args);

var statestore = builder.AddDaprStateStore("pizzastatestore");
var pubsubComponent = builder.AddDaprPubSub("pizzapubsub");
```



#### Add Dapr sidecar to .NET Aspire resources

Dapr uses the [sidecar pattern](https://docs.dapr.io/concepts/dapr-services/sidecar/). The Dapr sidecar runs alongside your app as a lightweight, portable, and stateless HTTP server that listens for incoming HTTP requests from your app.

To add a sidecar to a .NET Aspire resource, call the [WithDaprSidecar](https://learn.microsoft.com/en-us/dotnet/api/aspire.hosting.idistributedapplicationresourcebuilderextensions.withdaprsidecar) method on it. The `appId` parameter is the unique identifier for the Dapr application, but it's optional. If you don't provide an `appId`, the parent resource name is used instead. Also add reference to `statestore`

```c#
using Aspire.Hosting.Dapr;

var builder = DistributedApplication.CreateBuilder(args);

var statestore = builder.AddDaprStateStore("pizzastatestore");
var pubsubComponent = builder.AddDaprPubSub("pizzapubsub");

builder.AddProject<Projects.PizzaOrder>("pizzaorderservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-order",
        DaprHttpPort = 3501
    })
    .WithReference(statestore)
    .WithReference(pubsubComponent);

builder.AddProject<Projects.PizzaKitchen>("pizzakitchenservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-kitchen",
        DaprHttpPort = 3503
    })
    .WithReference(pubsubComponent);

builder.AddProject<Projects.PizzaStorefront>("pizzastorefrontservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-storefront",
        DaprHttpPort = 3502
    })
    .WithReference(pubsubComponent);

builder.AddProject<Projects.PizzaDelivery>("pizzadeliveryservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-delivery",
        DaprHttpPort = 3504
    })
    .WithReference(pubsubComponent);

builder.Build().Run();
```

## Application changes

Aspire declarative PubSub does not work with Aspire (not without dapr component yaml files). Therefor the code must be changed to programmatic PubSub

### Changes in `PizzaOrder`
#### In program.cs:

```c#
using PizzaOrder.Services;

var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddControllers().AddDapr();
builder.Services.AddSingleton<IOrderStateService, OrderStateService>();

var app = builder.Build();

app.MapDefaultEndpoints();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Dapr will send serialized event object vs. being raw CloudEvent
app.UseCloudEvents();

// needed for Dapr pub/sub routing
app.MapSubscribeHandler();

app.MapControllers();
app.Run();
```



#### In OrderController.cs

```
    [HttpPost("/orders-sub")]
    [Topic("pizzapubsub", "orders")]
    public async Task<IActionResult> HandleOrderUpdate(Order cloudEvent)
    {
        _logger.LogInformation("Received order update for order {OrderId}", 
            cloudEvent.OrderId);

        var result = await _orderStateService.UpdateOrderStateAsync(cloudEvent);
        return Ok();
    }
```



#### CloudEvent.cs

Delete `CloudEvent`

### Dapr ressources

Delete the `resources` folder


## Test the service

Add the `Endpoints.http` in the `start-here` folder to the solution.

Open `Endpoints.http` and create a new order sending the request on `Direct Pizza Store Endpoint (for testing)`, similar to what was done previous challenge.

In Aspire Dashboard: Navigate to the `pizzaorderservice` Console logs, where you should see the following logs:

```
2025-02-05T12:43:21 info: Microsoft.Hosting.Lifetime[14]
2025-02-05T12:43:21       Now listening on: http://localhost:50222
2025-02-05T12:43:21 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T12:43:21       Application started. Press Ctrl+C to shut down.
2025-02-05T12:43:21 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T12:43:21       Hosting environment: Development
2025-02-05T12:43:21 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T12:43:21       Content root path: C:\Dropbox\SourceCode\dapr\02-DaprAspire\dapr-workshop-aspire\start-here\PizzaOrder
2025-02-05T12:43:29 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:29       Received order update for order 123
2025-02-05T12:43:29 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:29       Updated state for order 123 - Status: validating
2025-02-05T12:43:30 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:30       Received order update for order 123
2025-02-05T12:43:30 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:30       Updated state for order 123 - Status: processing
2025-02-05T12:43:32 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:32       Received order update for order 123
2025-02-05T12:43:32 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:32       Updated state for order 123 - Status: confirmed
2025-02-05T12:43:33 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:33       Received order update for order 123
2025-02-05T12:43:33 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:33       Updated state for order 123 - Status: cooking_preparing_ingredients
2025-02-05T12:43:35 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:35       Received order update for order 123
2025-02-05T12:43:35 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:35       Updated state for order 123 - Status: cooking_making_dough
2025-02-05T12:43:38 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:38       Received order update for order 123
2025-02-05T12:43:38 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:38       Updated state for order 123 - Status: cooking_adding_toppings
2025-02-05T12:43:40 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:40       Received order update for order 123
2025-02-05T12:43:40 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:40       Updated state for order 123 - Status: cooking_baking
2025-02-05T12:43:45 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:45       Received order update for order 123
2025-02-05T12:43:45 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:45       Updated state for order 123 - Status: cooking_quality_check
2025-02-05T12:43:46 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:46       Received order update for order 123
2025-02-05T12:43:46 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:46       Updated state for order 123 - Status: cooked
2025-02-05T12:43:46 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:46       Received order update for order 123
2025-02-05T12:43:46 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:46       Updated state for order 123 - Status: delivery_finding_driver
2025-02-05T12:43:49 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:49       Received order update for order 123
2025-02-05T12:43:49 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:49       Updated state for order 123 - Status: delivery_driver_assigned
2025-02-05T12:43:50 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:50       Received order update for order 123
2025-02-05T12:43:50 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:50       Updated state for order 123 - Status: delivery_picked_up
2025-02-05T12:43:52 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:52       Received order update for order 123
2025-02-05T12:43:52 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:52       Updated state for order 123 - Status: delivery_on_the_way
2025-02-05T12:43:57 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:57       Received order update for order 123
2025-02-05T12:43:57 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:57       Updated state for order 123 - Status: delivery_arriving
2025-02-05T12:43:59 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:43:59       Received order update for order 123
2025-02-05T12:43:59 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:43:59       Updated state for order 123 - Status: delivery_at_location
2025-02-05T12:44:00 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T12:44:00       Received order update for order 123
2025-02-05T12:44:00 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T12:44:00       Updated state for order 123 - Status: delivered
```

### Traces
In Aspire Dashboard: Navigate to Traces and select `pizzastorefrontservice: POST Storefront/order`

Look for pub sub in the trace :-)
