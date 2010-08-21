.. _tutorial:

Tutorial
--------

A RepRep report is a hierarchical collection of nodes. There are three types of nodes:

1. **Generic nodes** holding python data, such as numpy arrays.
2. **Binary nodes** holding file data, such as PNG images.
3. **Figure nodes** that describe an arrangement of the data suitable to create a quick report for preview.

The following is the minimal example of a report. 
We add one data node called ``'covariance'``, and one figure.
The figure contains one subfigure that displays the node ``'covariance'``.
The ``display='posneg'`` parameters is a hint on how the covariance 
should be displayed. (see HTML and PDF results)::

	from reprep import Report
	
	report = Report()
	
	# add a node called "covariance" with the data M
	report.data('covariance', M)
	
	# add a figure with one subfigure; 
	# 'posneg' is one of the default formatters
	f =  report.figure()
	f.sub('covariance', caption='The covariance', display='posneg')

Under the hood, the node structure has been created as follows::

	report
	|_ covariance         numpy array
	|  |_ as_posneg       image/png data
	|_ figure
	   |_ sub             '../covariance/as_posneg'

As you can see, a new node ``'as_posneg'`` has been created as a child node to covariance

Of course, you can create your own data visualizations, and RepRep makes it easy.

The next example is largely equivalent to the former, with the only change that this time we use ``pylab`` to display the covariance. (see HTML and PDF results)::::

	from reprep import Report
	
	report = Report()
	cov = report.data('covariance', M)
	
	# Attach a png file to the 'covariance' node.
	# Note the idiomatic 'with' construct, explained below.
	with cov.data_file(id='display', mime='image/png') as filename:
		pylab.imsave(M, filename)
		
	f =  report.figure()
	f.sub('covariance', caption='The covariance')
 
Note the idiomatic 'with' construct above. In the block, just write to the 
given ``filename``, and RepRep will take care of generating a temporary file name,
and copying the results into the report.

Finally, here's a slightly more complicated example, in which we attach
two plots

* RepRep's interface encourages you to add the source data to the report other than the 
