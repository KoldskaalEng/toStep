This is a tool for converting grids of cartesian coordinates into Bsplines surfaces and saving a stepfile, of the results. That's it. 

**Run it like this: (bash)**
```bash
python make_step.py test_prop.txt
```

It assumes that your points are formatted like this:   

> Surface definition example:
>
> ```text
> Surface0(
>   Section0(
>     ( point0 x ; point0 y ; point0 z)
>     ( point1 x ; point1 y ; point1 z)
>     ( point2 x ; point2 y ; point2 z)
>     etc.
>     ( pointn x ; pointn y ; pointn z)
>   )SectionEnd
>   Section1(
>     ~ section 1 points ~
>   )SectionEnd
>   ~ add more sections ~
> )SurfaceEnd
> ~ add more surfaces ~
> ```
> NB! Indentation added for clarity

It is assumed that the points given in the file are **points on the surface**. The script determines appropriate **controlnode** locations to reproduce the surface. The final Bspline surfaces have the same polynomial degree along both *u* and *v*. Every section belonging to the same surface must contain the same number of points. 

**Adjust polynomial degree like this: (bash)**
```bash
python make_step.py test_prop.txt --degree 5
```
Or simply 
```bash
python make_step.py test_prop.txt -p 5
```

**Change the name of the step-file like this: (bash)**
```bash
python make_step.py test_prop.txt --stpfilename some_other_name
```
This script is not intended for commercial use.