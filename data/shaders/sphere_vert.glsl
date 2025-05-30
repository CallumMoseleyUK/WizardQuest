#version 330 core

// Input vertex data, different for all executions of this shader.
layout(location = 0) in vec3 vertexPosition_modelspace;
layout(location = 1) in vec2 vertexUV;

// Output data ; will be interpolated for each fragment.
out vec4 vertexColor;

// Values that stay constant for the whole mesh.
uniform mat4 MVP;
uniform vec3 OFFSET;

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main(){

	vec3 position_offset = vertexPosition_modelspace.xyz+OFFSET.xyz;
	// Output position of the vertex, in clip space : MVP * position
	gl_Position =  MVP * vec4(position_offset,1);
	
    vec3 hsvColor = vec3(position_offset[2],1.0,1.0);
    vec3 rgbColor = hsv2rgb(hsvColor);
	vertexColor = vec4(rgbColor,1.0);
}