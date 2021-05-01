import React from 'react';

const WeekHeading = (props) => {
	return (
		<div className='col'>
			<h1>{props.week}</h1>
		</div>
	);
};

export default WeekHeading;