# Aspire - Challenge 4 - Workflow
## Prepare

Clone the repository: `https://github.com/kbr-ucl/dapr-workshop-csharp`

Checkout branch `challenge-4`

Create a new branch `aspire-challenge-4`


### Add  .NET Aspire Orchestration Support

- Right click `PizzaStorefront`project and add  `.NET Aspire Orchestration Support`

- Right click `PizzaKitchen`project and add  `.NET Aspire Orchestration Support`

- Right click `PizzaDelivery`project and add  `.NET Aspire Orchestration Support`

- Right click `PizzaOrder`project and add  `.NET Aspire Orchestration Support`

- Right click `PizzaWorkflow`project and add  `.NET Aspire Orchestration Support`



## Dapr Resources

Aspire version 1.15.4 uses Dapr resources files.

We will use Programmatic Pub/sub API subscription (Link: [Pub/sub API subscription types](https://docs.dapr.io/developing-applications/building-blocks/pubsub/subscription-methods/#pubsub-api-subscription-types) )



## Hosting integration

In your .NET Aspire solution, to integrate Dapr and access its types and APIs, add the CommunityToolkit.Aspire.Hosting.Dapr NuGet package in the `DaprWorkshop.AppHost` project.

```powershell
dotnet add package CommunityToolkit.Aspire.Hosting.Dapr
```

### Nuget update

Use Nuget Packet Manager for solution to update packets.

### In folder DaprWorkshop.AppHost add changes to `Program.cs`

#### Add Dapr sidecar to .NET Aspire resources

Dapr uses the [sidecar pattern](https://docs.dapr.io/concepts/dapr-services/sidecar/). The Dapr sidecar runs alongside your app as a lightweight, portable, and stateless HTTP server that listens for incoming HTTP requests from your app.

To add a sidecar to a .NET Aspire resource, call the [WithDaprSidecar](https://learn.microsoft.com/en-us/dotnet/api/aspire.hosting.idistributedapplicationresourcebuilderextensions.withdaprsidecar) method on it. The `appId` parameter is the unique identifier for the Dapr application, but it's optional. If you don't provide an `appId`, the parent resource name is used instead. Also add reference to `ResourcesPaths`  to include the Dapr resources yaml files.

```c#
using CommunityToolkit.Aspire.Hosting.Dapr;
using Projects;
using System.Collections.Immutable;

var builder = DistributedApplication.CreateBuilder(args);

builder.AddProject<PizzaOrder>("pizzaorderservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-order",
        DaprHttpPort = 3501,
        ResourcesPaths = ImmutableHashSet.Create("../resources")
    });


builder.AddProject<PizzaKitchen>("pizzakitchenservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-kitchen",
        DaprHttpPort = 3503,
        ResourcesPaths = ImmutableHashSet.Create("../resources")
    });


builder.AddProject<PizzaStorefront>("pizzastorefrontservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-storefront",
        DaprHttpPort = 3502,
        ResourcesPaths = ImmutableHashSet.Create("../resources")
    });


builder.AddProject<PizzaDelivery>("pizzadeliveryservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-delivery",
        DaprHttpPort = 3504,
        ResourcesPaths = ImmutableHashSet.Create("../resources")
    });


builder.AddProject<PizzaWorkflow>("pizzaworkflowservice")
    .WithDaprSidecar(new DaprSidecarOptions
    {
        AppId = "pizza-workflow",
        DaprHttpPort = 3505,
        ResourcesPaths = ImmutableHashSet.Create("../resources")
    });


builder.Build().Run();
```

## Application changes

Since we are using Aspire component files (resources) we can have to return switch Dapr programmatic PubSub. 

### Changes in `PizzaOrder`

#### Changes to `OrderController.cs`

Change `HandleOrderUpdate` to programmatic pub/sub 

```c#
    [HttpPost("/orders-sub")]
    [Topic("pizzapubsub", "orders")] // Programmatic Dapr pub/sub topic 
    public async Task<IActionResult> HandleOrderUpdate(Order cloudEvent)
    {
        _logger.LogInformation("Received order update for order {OrderId}", 
            cloudEvent.OrderId);

        var result = await _orderStateService.UpdateOrderStateAsync(cloudEvent);
        return Ok();
    }
}
```



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

// Needed for Programmatic Dapr pub/sub routing
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


## Test the service

Add the `Endpoints.http` in the `start-here` folder to the solution.

Open `Endpoints.http` and start a new workflow sending the request on `Start a new pizza order workflow`

Then send the request `Validate pizza (approve)`

In Aspire Dashboard: Navigate to the `pizzaworkflowservice` Console logs, where you should see the following logs:

```
2025-02-05T19:32:33 info: Dapr.Workflow.WorkflowLoggingService[0]
2025-02-05T19:32:33       WorkflowLoggingService started
2025-02-05T19:32:33 info: Dapr.Workflow.WorkflowLoggingService[0]
2025-02-05T19:32:33       List of registered workflows
2025-02-05T19:32:33 info: Dapr.Workflow.WorkflowLoggingService[0]
2025-02-05T19:32:33       PizzaOrderingWorkflow
2025-02-05T19:32:33 info: Dapr.Workflow.WorkflowLoggingService[0]
2025-02-05T19:32:33       List of registered activities:
2025-02-05T19:32:33 info: Dapr.Workflow.WorkflowLoggingService[0]
2025-02-05T19:32:33       StorefrontActivity
2025-02-05T19:32:33 info: Dapr.Workflow.WorkflowLoggingService[0]
2025-02-05T19:32:33       CookingActivity
2025-02-05T19:32:33 info: Dapr.Workflow.WorkflowLoggingService[0]
2025-02-05T19:32:33       ValidationActivity
2025-02-05T19:32:33 info: Dapr.Workflow.WorkflowLoggingService[0]
2025-02-05T19:32:33       DeliveryActivity
2025-02-05T19:32:33 info: Microsoft.DurableTask[1]
2025-02-05T19:32:33       Durable Task gRPC worker starting.
2025-02-05T19:32:33 info: Microsoft.Hosting.Lifetime[14]
2025-02-05T19:32:33       Now listening on: http://localhost:58245
2025-02-05T19:32:33 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T19:32:33       Application started. Press Ctrl+C to shut down.
2025-02-05T19:32:33 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T19:32:33       Hosting environment: Development
2025-02-05T19:32:33 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T19:32:33       Content root path: C:\Dropbox\SourceCode\dapr\02-DaprAspire\dapr-workshop-aspire\start-here\PizzaWorkflow
2025-02-05T19:32:33 info: Microsoft.DurableTask[4]
2025-02-05T19:32:33       Sidecar work-item streaming connection established.
2025-02-05T19:32:35 info: PizzaWorkflow.Controllers.WorkflowController[0]
2025-02-05T19:32:35       Starting workflow for order 1
2025-02-05T19:32:36 info: PizzaWorkflow.Controllers.WorkflowController[0]
2025-02-05T19:32:36       Workflow started successfully for order 1
2025-02-05T19:32:36 info: PizzaWorkflow.Activities.StorefrontActivity[0]
2025-02-05T19:32:36       Starting ordering process for order 1
2025-02-05T19:32:41 info: PizzaWorkflow.Activities.StorefrontActivity[0]
2025-02-05T19:32:41       Order 1 processed with status confirmed
2025-02-05T19:32:41 info: PizzaWorkflow.Activities.CookingActivity[0]
2025-02-05T19:32:41       Starting cooking process for order 1
2025-02-05T19:32:55 info: PizzaWorkflow.Activities.CookingActivity[0]
2025-02-05T19:32:55       Order 1 cooked with status cooked
2025-02-05T19:32:55 info: PizzaWorkflow.Activities.ValidationActivity[0]
2025-02-05T19:32:55       Starting validation process for order 1
2025-02-05T19:32:55 info: PizzaWorkflow.Activities.ValidationActivity[0]
2025-02-05T19:32:55       Validation state saved for order 1
2025-02-05T19:33:00 info: PizzaWorkflow.Controllers.WorkflowController[0]
2025-02-05T19:33:00       Raising validation event for order 1. Approved: True
2025-02-05T19:33:00 info: PizzaWorkflow.Controllers.WorkflowController[0]
2025-02-05T19:33:00       Validation event raised successfully for order 1
2025-02-05T19:33:00 info: PizzaWorkflow.Activities.DeliveryActivity[0]
2025-02-05T19:33:00       Starting delivery process for order 1
2025-02-05T19:33:13 info: PizzaWorkflow.Activities.DeliveryActivity[0]
2025-02-05T19:33:13       Order 1 delivered with status delivered
```

In Aspire Dashboard: Navigate to the `pizzaorderservice` Console logs, where you should see the following logs:

```
2025-02-05T19:32:32 info: Microsoft.Hosting.Lifetime[14]
2025-02-05T19:32:32       Now listening on: http://localhost:58238
2025-02-05T19:32:32 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T19:32:32       Application started. Press Ctrl+C to shut down.
2025-02-05T19:32:32 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T19:32:32       Hosting environment: Development
2025-02-05T19:32:32 info: Microsoft.Hosting.Lifetime[0]
2025-02-05T19:32:32       Content root path: C:\Dropbox\SourceCode\dapr\02-DaprAspire\dapr-workshop-aspire\start-here\PizzaOrder
2025-02-05T19:32:37 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:37       Received order update for order 1
2025-02-05T19:32:37 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:37       Updated state for order 1 - Status: validating
2025-02-05T19:32:38 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:38       Received order update for order 1
2025-02-05T19:32:38 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:38       Updated state for order 1 - Status: processing
2025-02-05T19:32:40 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:40       Received order update for order 1
2025-02-05T19:32:40 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:40       Updated state for order 1 - Status: confirmed
2025-02-05T19:32:41 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:41       Received order update for order 1
2025-02-05T19:32:41 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:41       Updated state for order 1 - Status: cooking_preparing_ingredients
2025-02-05T19:32:43 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:43       Received order update for order 1
2025-02-05T19:32:43 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:43       Updated state for order 1 - Status: cooking_making_dough
2025-02-05T19:32:46 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:46       Received order update for order 1
2025-02-05T19:32:46 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:46       Updated state for order 1 - Status: cooking_adding_toppings
2025-02-05T19:32:48 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:48       Received order update for order 1
2025-02-05T19:32:49 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:49       Updated state for order 1 - Status: cooking_baking
2025-02-05T19:32:54 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:54       Received order update for order 1
2025-02-05T19:32:54 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:54       Updated state for order 1 - Status: cooking_quality_check
2025-02-05T19:32:55 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:32:55       Received order update for order 1
2025-02-05T19:32:55 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:32:55       Updated state for order 1 - Status: cooked
2025-02-05T19:33:00 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:33:00       Received order update for order 1
2025-02-05T19:33:00 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:33:00       Updated state for order 1 - Status: delivery_finding_driver
2025-02-05T19:33:02 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:33:02       Received order update for order 1
2025-02-05T19:33:02 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:33:02       Updated state for order 1 - Status: delivery_driver_assigned
2025-02-05T19:33:03 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:33:03       Received order update for order 1
2025-02-05T19:33:03 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:33:03       Updated state for order 1 - Status: delivery_picked_up
2025-02-05T19:33:05 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:33:05       Received order update for order 1
2025-02-05T19:33:05 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:33:05       Updated state for order 1 - Status: delivery_on_the_way
2025-02-05T19:33:10 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:33:10       Received order update for order 1
2025-02-05T19:33:10 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:33:10       Updated state for order 1 - Status: delivery_arriving
2025-02-05T19:33:12 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:33:12       Received order update for order 1
2025-02-05T19:33:12 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:33:12       Updated state for order 1 - Status: delivery_at_location
2025-02-05T19:33:13 info: PizzaOrder.Controllers.OrderController[0]
2025-02-05T19:33:13       Received order update for order 1
2025-02-05T19:33:13 info: PizzaOrder.Services.OrderStateService[0]
2025-02-05T19:33:13       Updated state for order 1 - Status: delivered
```



### Traces

In Aspire Dashboard: Navigate to Traces and select `pizzaworkflowservice: POST Workflow/start-order`

Observe the activities calls.
