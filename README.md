# solar-panel-detection
RoofTop Solar Panel Detection using Deep Learning
Project ID: RSPD-1222

Project Name: RoofTop Solar Panel Detection using Deep Learning


Workflow of this notebook
1) Introducing the Problem
2) Understanding the Dataset
3) Importing necessary libraries and modules for this notebook
4) Exploratory Analysis & Data Scaling
5) Building & Tuning our CNN Model
6) Model Evaluation & Results
7) Task for You

Introduction to the problem
Why should solar panels be detected?
Presently, 1% of the electricity produced worldwide comes from solar energy. In fact, predictions for solar energy production indicate a possible 65-fold increase in output by 2050, making solar energy one of the world's greatest sources of energy at that point. Thirty percent of this energy is thought to be produced by solar photovoltaic, or solar PV, power systems mounted on rooftops. Solar PV power has already started to take on a more and bigger part in the generation of electricity in the US in recent years. Solar energy production increased by 75,123 GWh or 39 times between 2008 and 2017, or a 39-fold increase.

Here's an overview on the global growth -

Capture218.jpg

Credits : Bloomberg

Granular data on distributed rooftop solar PV is becoming increasingly important as solar photovoltaic (PV) becomes a significant segment of the energy industry. An imagery-based solar panel recognition algorithm that can be used to create detailed databases of installations and their power capacity would be extremely helpful to solar power suppliers and consumers, urban planners, grid system operators, and energy policy makers. The fact that solar panel installers typically keep installation details to themselves is another factor in solar panel detection. A well-known solar panel detecting technique or algorithm is therefore urgently needed. However, there hasn't been much effort done to identify solar panels in aerial or satellite photographs.

We first require a labelled data-set of satellite images in order to create an algorithm that can recognise solar panels from aerial or satellite imagery.

Understanding the Dataset
Here are a few snippets from the dataset - Images containing Solar Panels

Here are a few snippets from the dataset - Images NOT containing Solar Panels

When examining the photographs themselves, it is clear that solar panels frequently have rectangular shapes with distinct angles and borders. However, the whole pictures that include solar PV do not necessarily have a same structure. The solar panels are not always at the centre of images, which come in a range of sizes and hues. Additionally, the background scenery in the photographs of the two classes is also not uniform. Both classes contain illustrations of home swimming pools, pavement, grass, and rooftops. A model should also be able to predict the same class independent of the orientation of each image.
