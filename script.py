from pyscript import Element, display
import micropip
import io
import base64

async def install_matplotlib():
    await micropip.install("matplotlib")


async def calculateBOP(event):

    await install_matplotlib()

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


    try:

        # Get values from input fields
        fixed_cost = float(Element("fixedCost").value) if Element("fixedCost").value else 0
        variable_cost = float(Element("variableCost").value) if Element("variableCost").value else 0
        price_per_unit = float(Element("pricePerUnit").value) if Element("pricePerUnit").value else 0

    except ValueError:

        result_text = "Invalid number! Please try again!"

        # Clear inputs on error
        Element("fixedCost").element.value = ""
        Element("variableCost").element.value = ""
        Element("pricePerUnit").element.value = ""
        Element("bopSpan").element.innerHTML = result_text
        return    



    # Calculate break-even point
    temp_val = price_per_unit - variable_cost

    if not temp_val == 0:
        bop = fixed_cost / temp_val
        result_text = f"{bop:.2f}"
    else:
        bop = None
        result_text = "Break-Even Point is Undefined"

    # Update the result span with the calculated value
    Element("bopSpan").element.innerHTML = result_text

    # Prepare data for the chart
    if bop is not None:

        thirtyPercentOfBop = bop * 0.30

        units = np.arange(0, int(bop) + thirtyPercentOfBop, 1) # xtending the range of units sold by 30% units above the break-even point (BEP)
        
        revenue = price_per_unit * units    # calculating the revenue

        costs = fixed_cost + variable_cost * units  # calculating the total costs

        # Create chart with larger figure size
        fig, ax = plt.subplots(figsize=(8, 4))  
        ax.plot(units, revenue, label='Revenue', color='blue')
        ax.plot(units, costs, label='Total Costs', color='red')
        ax.axvline(x=bop, color='green', linestyle='--', label='Break-Even Point')
        ax.set_title('Break-Even Analysis')
        ax.set_xlabel('Units Sold')
        ax.set_ylabel('Pesos')
        ax.legend()

        # Save the plot to a PNG in memory
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        # Convert PNG to base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        img_src = f"data:image/png;base64,{img_base64}"

        # Draw the image on the canvas
        canvas = Element("bepChart").element
        context = canvas.getContext('2d')
        context.clearRect(0, 0, canvas.width, canvas.height)  # Clear the canvas

        # Create an Image instance
        img = Element("image")
        img.element.src = img_src

        # Use a callback to draw the image once it is loaded
        def on_image_load(event):
            # Adjusting to fit the canvas
            context.drawImage(img.element, 0, 0, canvas.width, canvas.height)

        img.element.onload = on_image_load

button = Element("calculate")
button.element.onclick = calculateBOP