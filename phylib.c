#include "phylib.h"

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ) 
{
    //initialize and allocate memory for the new object
    phylib_object *newStill_phylib_object = (phylib_object*)calloc(1, sizeof(phylib_object));

    // checking for an invalide calloc operation
    if(newStill_phylib_object == NULL) 
    {
        return NULL;
    }

    // set the objects type to a still ball
    newStill_phylib_object->type = PHYLIB_STILL_BALL;
    // set the object number to the given number
    newStill_phylib_object->obj.still_ball.number = number;

    //check if the position is valid
    if(pos != NULL) 
    {
        // set the position for x and y of a still ball
        newStill_phylib_object->obj.still_ball.pos = (*pos);
    }else
    // otherwise set the values to zero
    {
        newStill_phylib_object->obj.still_ball.pos = (phylib_coord){0, 0};
    }

    // return the new object
    return newStill_phylib_object;
}

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ) 
{
    // same operations as above but for a rolling ball upto the position
    phylib_object *newRolling_phylib_object = (phylib_object*)calloc(1, sizeof(phylib_object));

    if(newRolling_phylib_object == NULL) 
    {
        return NULL;
    }

    newRolling_phylib_object->type = PHYLIB_ROLLING_BALL;
    newRolling_phylib_object->obj.rolling_ball.number = number;

    if(pos != NULL) 
    {
        newRolling_phylib_object->obj.rolling_ball.pos = (*pos);
    } else
    {
        newRolling_phylib_object->obj.rolling_ball.pos = (phylib_coord){0, 0};
    }

    // sets the value of the velocity to either the given vel or zero 
    if(vel != NULL)
    {
        newRolling_phylib_object->obj.rolling_ball.vel = (*vel);
    } else
    {
        newRolling_phylib_object->obj.rolling_ball.vel = (phylib_coord){0, 0};
    }

    // sets the value of the acceleration to either the given acc or zero 
    if(acc != NULL)
    {
        newRolling_phylib_object->obj.rolling_ball.acc = (*acc);
    } else
    {
        newRolling_phylib_object->obj.rolling_ball.acc = (phylib_coord){0, 0};
    }

        
    return newRolling_phylib_object;
}


phylib_object *phylib_new_hole( phylib_coord *pos ) 
{
    // same operations as above for a new hole
    phylib_object *newHole_phylib_object = (phylib_object*)calloc(1, sizeof(phylib_object));

    if(newHole_phylib_object == NULL) 
    {
        return NULL;
    }

    newHole_phylib_object->type = PHYLIB_HOLE;

    if(pos != NULL) 
    {
        newHole_phylib_object->obj.hole.pos = (*pos);
    }

    return newHole_phylib_object;
}


phylib_object *phylib_new_hcushion( double y ) 
{
    // same operations as above for a new horizontal cushion
    phylib_object *newHCushion_phylib_object = (phylib_object*)calloc(1, sizeof(phylib_object));

    
    if(newHCushion_phylib_object == NULL)
    {
        return NULL;
    }

    newHCushion_phylib_object->type = PHYLIB_HCUSHION;
    newHCushion_phylib_object->obj.hcushion.y = y;

    return newHCushion_phylib_object;
}

phylib_object *phylib_new_vcushion( double x ) 
{
    // same operations as above for a new vertical cushion
    phylib_object *newVCushion_phylib_object = (phylib_object*)calloc(1, sizeof(phylib_object));

    if(newVCushion_phylib_object == NULL) 
    {
        return NULL;
    }

    newVCushion_phylib_object->type = PHYLIB_VCUSHION;
    newVCushion_phylib_object->obj.vcushion.x = x;

    return newVCushion_phylib_object;
}

phylib_table *phylib_new_table( void ) 
{
    // create a new table object
    phylib_table *new_phylib_table = (phylib_table*)calloc(1, sizeof(phylib_table));

    // check for an invalide calloc operation
    if(new_phylib_table == NULL) 
    {
        return NULL;
    }

    // initialize all values int the table to be null    
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        new_phylib_table->object[i] = NULL;
    }

    // set the tables time to zero
    new_phylib_table->time = 0.0;

    // create two new h-cushions
    new_phylib_table->object[0] = phylib_new_hcushion(0.0);
    new_phylib_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    // create two new v-cushions
    new_phylib_table->object[2] = phylib_new_vcushion(0.0);
    new_phylib_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    
    // calculate the and store the 6 new hole positions
    phylib_coord topLeft = {.x = 0.0, .y = 0.0};
    phylib_coord topRight = {.x = 0, .y = PHYLIB_TABLE_WIDTH};
    phylib_coord bottomLeft = {.x = 0, .y = PHYLIB_TABLE_LENGTH};
    phylib_coord bottomRight = {.x = PHYLIB_TABLE_WIDTH, .y = PHYLIB_TABLE_LENGTH};
    phylib_coord middleLeft = {.x = (PHYLIB_TABLE_LENGTH / 2), .y = 0};
    phylib_coord middleRight = {.x = PHYLIB_TABLE_WIDTH, .y = (PHYLIB_TABLE_LENGTH / 2)};
    
    // assign the new hole postions to their index
    new_phylib_table->object[4] = phylib_new_hole(&topLeft);
    new_phylib_table->object[5] = phylib_new_hole(&topRight);

    new_phylib_table->object[6] = phylib_new_hole(&bottomLeft);

    new_phylib_table->object[7] = phylib_new_hole(&middleLeft);
    new_phylib_table->object[8] = phylib_new_hole(&middleRight);

    new_phylib_table->object[9] = phylib_new_hole(&bottomRight);

    // return the table
    return new_phylib_table;
}

/*------ Part Two ------*/
void phylib_copy_object( phylib_object **dest, phylib_object **src ) 
{
    // check if the incoming object is valid or not
    if(*src == NULL) 
    {
        // set new object to null and return
        *dest = NULL;  
        return;
    }

    // initialize the outgoing object
    *dest =  (phylib_object*)calloc(1, sizeof(phylib_object));

    // check if calloc operation was valid
    if(*dest == NULL) 
    {
        return;
    }

    // copy over the contents from incoming oject to the outgoig object
    memcpy(*dest, *src, sizeof(phylib_object));

}


phylib_table *phylib_copy_table( phylib_table *table) 
{
    // check if table is valid
    if(table == NULL)
    {
        return NULL;
    }

    // create a table and check the malloc operation was valid
    phylib_table *new_phylib_table = malloc(sizeof(phylib_table));
    if(new_phylib_table == NULL)
    {
        return NULL;
    }

    // set the tables time to the given time
    new_phylib_table->time = table->time;

    // loop through each object in the table
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        // call the copy object function to copy the objects into the new table
        phylib_copy_object(&new_phylib_table->object[i], &table->object[i]);
    }

    // return the new table
    return new_phylib_table;
}

void phylib_add_object( phylib_table *table, phylib_object *object ) 
{
    // used to check if the table and object are valid
    if(table == NULL || object == NULL) 
    {
        return;
    }

    // loops through the table and adds a new object to the first occurence of a null index
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        if(table->object[i] == NULL)
        {
            table->object[i] = object;
            return;
        }
    }
}

void phylib_free_table( phylib_table *table)
{
    if(table == NULL) 
    {
        return;
    }

    // used ot loop through the table and free the memory for each object
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
    {
        // checks if the object is valid
        if(table->object[i] != NULL)
        {
            free(table->object[i]);
        }
    }
    //frees the table
    free(table);
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) 
{
    phylib_coord updated_phylib_cord;
    double x_final = c1.x - c2.x;;
    double y_final = c1.y - c2.y;

    // finds the subtraction between two coordinates
    updated_phylib_cord = (phylib_coord){.x = x_final, .y = y_final};

    return updated_phylib_cord;
}

double phylib_length( phylib_coord c )
{
    // premforms the pythagreom theroem: a^2 + b^2 = c^2
    double pyth_len = sqrt((c.x * c.x) + (c.y * c.y));
    
    return pyth_len;
}

double phylib_dot_product( phylib_coord a, phylib_coord b )
{
    // prefroms the dot product: x1 * x2 + y1 * y2
    double dot_prod = (a.x * b.x) + (a.y * b.y);

    return dot_prod;
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) 
{
    if(obj1 == NULL || obj2 == NULL)
    {
        return -1.0;
    }

    // checks if the given object1 is the required type needed
    if(obj1->type != PHYLIB_ROLLING_BALL)
    {
        return -1.0;
    }

    double distance = 0.0;

    // preforms a diffrent functions based on the type of the second object
    // used to find the distance between the two objects 
    switch(obj2->type) {
        case PHYLIB_ROLLING_BALL:
        // calls the two functions sub and length and subtracts the ball diameter to find the distance
          distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER;
          break;

        case PHYLIB_STILL_BALL:
        // calls the two functions sub and length and subtracts the ball diameter to find the distance
          distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;
          break;

        case PHYLIB_HOLE:
        // calls the two functions sub and length and subtracts the hole radius to find the distance
          distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
          break;

        case PHYLIB_VCUSHION:
        // finds the absolute value of the double produced from subtracting the two objects, then subtracts the ball radius 
          distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
          break;

        case PHYLIB_HCUSHION:
        // finds the absolute value of the double produced from subtracting the two objects, then subtracts the ball radius 
          distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
          break;
        default:
          distance = -1.0;
          break;
    }

    return distance;
}

/*------ Part Three ------*/
void phylib_roll( phylib_object *new, phylib_object *old, double time )
{
    if(new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) 
    {
        return;
    }

    // stores the old values of pos, vel, and acc
    phylib_coord p = {.x = old->obj.rolling_ball.pos.x, .y = old->obj.rolling_ball.pos.y};
    phylib_coord v = {.x = old->obj.rolling_ball.vel.x, .y = old->obj.rolling_ball.vel.y};
    phylib_coord a = {.x = old->obj.rolling_ball.acc.x, .y = old->obj.rolling_ball.acc.y};

    // finds the new position of the balls x and y coordinates
    new->obj.rolling_ball.pos.x = p.x + (v.x * time) + (0.5 * a.x * time * time);
    new->obj.rolling_ball.pos.y = p.y + (v.y * time) + (0.5 * a.y * time * time);

    // stores the new velocity coordinates
    phylib_coord newV = {.x = v.x + (a.x * time), .y = v.y + (a.y * time)};

    // checks if the signs flipped, zero if they have, and find the new vel and acc if they haven't
    if(flipped_signs(v.x, newV.x))
    {
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    } else 
    {
        new->obj.rolling_ball.vel.x = v.x + (a.x * time);
        new->obj.rolling_ball.acc.x = a.x;
    }

    if(flipped_signs(v.y, newV.y))
    {
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    } else 
    {
        new->obj.rolling_ball.vel.y = v.y + (a.y * time);
        new->obj.rolling_ball.acc.y = a.y;
    }
}


// helper function for phylib_roll
int flipped_signs(double a, double b)
{
    // signs havent flipped if true
    if(a * b >= 0)
    {
        return 0;
    }
    
    return 1;
}


unsigned char phylib_stopped( phylib_object *object )
{
    if(object == NULL)
    {
        return 0;
    }
    
    // checks if the speed of the ball is less then the specfied time in vel-epsilon
    if(phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON)
    {
        // update the balls type, number, and position
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        
        return 1;
    }

    return 0;
}

void phylib_bounce( phylib_object **a, phylib_object **b ) 
{
    if ((*a)->type != PHYLIB_ROLLING_BALL && (*b)->type != PHYLIB_ROLLING_BALL) 
    {
        return;
    }

    switch((*b)->type) {
        case PHYLIB_HCUSHION: 
        {
            // invert the values of vell and acc for the y pos
          (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y; 
          (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y; 
        }
          break;

        case PHYLIB_VCUSHION:
        {
            //invert the values of vel and acc for the x pos
          (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
          (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x; 
        }
          break;

        case PHYLIB_HOLE:
        
        // free the ball and clear it formt the table
          free((*a));
          (*a) = NULL;
          break;

        case PHYLIB_STILL_BALL:
        
        // update the ball type to rolling, the number, and the position 
          (*b)->type = PHYLIB_ROLLING_BALL;
          (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
          (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;

        case PHYLIB_ROLLING_BALL: {
        // find the needed values and store them
          phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
          phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
          double len = phylib_length(r_ab);
          phylib_coord n = {.x = r_ab.x / len, .y = r_ab.y / len};
          double v_rel_n = phylib_dot_product(v_rel, n);
          phylib_coord vel_update = {.x = v_rel_n * n.x, .y = v_rel_n * n.y};
          double speed_a = 0.0;
          double speed_b = 0.0;

        // invert the new vels for a and b
          (*a)->obj.rolling_ball.vel.x -= vel_update.x;
          (*a)->obj.rolling_ball.vel.y -= vel_update.y;
          (*b)->obj.rolling_ball.vel.x += vel_update.x;
          (*b)->obj.rolling_ball.vel.y += vel_update.y;

        // find and store the speed of the ball for a and b
          speed_a = phylib_length((*a)->obj.rolling_ball.vel);
          speed_b = phylib_length((*b)->obj.rolling_ball.vel);

        // find and store the new accelartion
          phylib_coord acc_epsilon_update_a = {.x = -(*a)->obj.rolling_ball.vel.x / speed_a * PHYLIB_DRAG, .y = -(*a)->obj.rolling_ball.vel.y / speed_a * PHYLIB_DRAG};
          phylib_coord acc_epsilon_update_b = {.x = -(*b)->obj.rolling_ball.vel.x / speed_b * PHYLIB_DRAG, .y = -(*b)->obj.rolling_ball.vel.y / speed_b * PHYLIB_DRAG};

        // check if speed is faster the vel-epsilon if so update the rolling ball
          if(speed_a > PHYLIB_VEL_EPSILON)
          {
            (*a)->obj.rolling_ball.acc = acc_epsilon_update_a;
          }

          if(speed_b > PHYLIB_VEL_EPSILON)
          {
            (*b)->obj.rolling_ball.acc = acc_epsilon_update_b;
          }

        }
          break;

          default:
            return;
    }
}


unsigned char phylib_rolling( phylib_table *t )
{
    int counter = 0;

    // used to count the amount of rolling balls
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if(t->object[i] != NULL) 
        {
            // checks if the ball is of the type rolling
            if(t->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                counter++;
            }
        }
    }

    return counter;
}

phylib_table *phylib_segment(phylib_table *table) {

    if (phylib_rolling(table) == 0) 
    {
        return NULL;
    }
    
    // table used to apply the logic of the functions and how it all interacts
    phylib_table *result_table = phylib_copy_table(table);
    
    // loops for a specified max time
    while (result_table->time < PHYLIB_MAX_TIME) 
    {        
        //loops for the max objects (26)
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) 
        {
            // checks the object is not null and its type is of rolling
            if (result_table->object[i] != NULL && result_table->object[i]->type == PHYLIB_ROLLING_BALL) 
            {
                // calls the rolling helper functions
                segment_rolling(result_table->object[i]);
                
            }
        }    

        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            if(result_table->object[i] != NULL && result_table->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                // calls the stopped helper function
                if (segment_stopped(result_table->object[i])) 
                {
                    // if so return the table
                    return result_table;
                }
                
                // calls the bounce helper function
                if (segment_bounce(result_table, i)) 
                {
                    // if all conditions are meet return the table
                    return result_table;
                }
            }
        }

        // for(int i = 0; i < PHYLIB_MAX_OBJECTS; i)
        // update the time     
        result_table->time += PHYLIB_SIM_RATE;
    }
    
    return result_table;
}

// Helper functions for phylib_segment

void segment_rolling(phylib_object *ball) 
{
    // create a new object to hold a value 
    phylib_object *temp_rolling_obj = NULL;

    // copy the object to the temp variable
    phylib_copy_object(&temp_rolling_obj, &ball);

    // appply the rolling logic for the ball
    phylib_roll(ball, temp_rolling_obj, PHYLIB_SIM_RATE);

    // free the temp variable
    free(temp_rolling_obj);
}

int segment_stopped(phylib_object *ball) 
{
    //check if the ball has stopped
    if (phylib_stopped(ball)) 
    {
        // if so return 1
        return 1; 
    }
    return 0; 
}

int segment_bounce(phylib_table *table, int i) 
{
    // loop through for the mac objects
    for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) 
    {
        // ensure that i and j dont equal and the objects not null
        if (i != j && table->object[j] != NULL) 
        {
            // check if the distance is less then zero 
            if (phylib_distance(table->object[i], table->object[j]) < 0.0) 
            {
                // if so apply the bounce logic and return 1
                phylib_bounce(&(table->object[i]), &(table->object[j]));
                table->time += PHYLIB_SIM_RATE;
                return 1;
            }
        }
    }
    return 0; 
}

char * phylib_object_string(phylib_object * object) 
{
    static char string[80];
    if (object == NULL) 
    {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object -> type) 
    {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object -> obj.still_ball.number,
            object -> obj.still_ball.pos.x,
            object -> obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object -> obj.rolling_ball.number,
            object -> obj.rolling_ball.pos.x,
            object -> obj.rolling_ball.pos.y,
            object -> obj.rolling_ball.vel.x,
            object -> obj.rolling_ball.vel.y,
            object -> obj.rolling_ball.acc.x,
            object -> obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        snprintf(string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object -> obj.hole.pos.x,
            object -> obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        snprintf(string, 80,
            "HCUSHION (%6.1lf)",
            object -> obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        snprintf(string, 80,
            "VCUSHION (%6.1lf)",
            object -> obj.vcushion.x);
        break;
    }
    return string;
}

