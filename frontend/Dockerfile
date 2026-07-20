#stage one building the frontend app 

# Start with this image that already contains Node.js and npm, Alpine which means a small Linux distribution.builder state stage one 
FROM node:20-alpine AS builder


WORKDIR /app


#copy only the package.json and package-lock.json 
COPY package*.json ./

RUN npm install


# Docker sees package.json and package-lock.json and only re-installs if they changed to make builds faster. The rest of the code is copied after this step 
COPY . .

#create the dist folder
RUN npm run build




#stage two Serve the built application with Nginx by copying the dist folder from stage one
FROM nginx:alpine


#Go to the stage named builder, take the react build from the dist folder and copy it to the nginx html folder so that it can be served by nginx.
COPY --from=builder /app/dist /usr/share/nginx/html

#to make it use my project's configuration not the default.
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

#starts the Nginx server.
CMD ["nginx", "-g", "daemon off;"]