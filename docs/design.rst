
report = Report()
report.data('covariance',  cov,       present='cov_mat', maxvalue=*)
report.data('information', pinv(cov), present='cov_mat', maxvalue=1)

with report.data_rep('information', 'text/pdf') as filename:

with report.version('information', 'png') as filename:

report.default


### Example Tx,Ty

Using pompous expressions: 

	report = Report('rangefinder')
		with report.child(id='covariance',class='covariance') as rep_cov:
			rep_cov.child(id='covariance', actual_cov)
			rep_cov.child(id='desc', mime='text/plain', 'This is the covariance matrix.')
			rep_cov.child(id='desc', mime='application/x-latex', 'This is the covariance matrix for $x$.')
			rep_cov.child(id='covariance', covariance_png)

		with report.child('tensor-report') as rep_tensors:
			rep_tensors.child(id)
		
		# add a table?
		
		# add 
		
		
Same thing later:
		
	report = Report('rangefinder', 'sensor-report')
		with report.child('covariance') as rep_cov:
			add_data(rep_cov, actual_cov)
			add_image_rep(rep_cov )
	
		rep_cov.desc('Covariance representation')
		rep_cov.set_numpy_rep(cov)
		
		with report.child('tensor-report') as r:
			r.child('T')
			r['Tx'] = Tx
			r.default_layout(rep_tensors, ['Tx','Ty','Ttheta'])
		
Adding comments:

	comment(report, '/rangefinder/covariance', '''Look at this! it's wonderful.''')
	comment(report,      '/camera/covariance', '''This did not work as well.''')
	
Adding comments, using YAML source:

	report.read_comments('file.yaml')
	
file.yaml:

	/rangefinder/covariance: |
		Look at this!, it's wonderful.
	/camera/covariance: |
		latex: |
			This did not work as well.

Display only the covariance

	report.extract('/*/covariance')


report.data('covariance',  cov)
report.data('information', pinv(cov))



report.display





A "node" is a container of nodes.

It has the following attributes:
	- `id` (unique among brothers)   (node_id)
	- `class` (list of classes)      (node_class)
	- `children`: list of nodes
	- `representation`: 
	
Optional attributes
	- `data` (string of type type)

	- `title`  "text/plain"  "theta histogram"
	- `title`  "text/latex"  "$\theta$ histogram "
	- desc
	- comment
	- children

A "resource" is a particular node that represents something tangible.
It has the following attributes:

	- document type ('image/png', 'text/latex')
	- content 

A resource has an id and a class. 


Example:

#vname  .vehicle-report    %node
	#vehicle .vehicle
		#numpy 
	
	#world
	
	#simulation 

	#tensor-natural .tensors .natural
	
		#iterations   %data/json   "1000"
		
		#Tx .tensor-display
			#png      %image/png    .color
				#desc  Colorcoded 
			#eps      %image/eps    .color
			#pdf      %image/pdf    .color
			#png      %image/png    .grayscale
			#eps      %image/eps    .grayscale
			#pdf      %image/pdf    .grayscale
			#numpy    %data/matlab    
			#matlab   %data/matlab
			#json     %data/json
		
		#Tx .tensor-display
		
		#lattice  %data/matlab
			.desc    text   "This is an array containing the poses at which it was evaluated"
		
		#raw-display .figure
			
	#raw-display .figure


A "figure" is a way to group some resources in figures / subfigures.



