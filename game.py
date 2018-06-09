class Game:
    def is_collision(self, collider, snake_segment, size):
        if (snake_segment.rect.y >= collider.rect.y and
                snake_segment.rect.y <= collider.rect.y + size):
            if (snake_segment.rect.x >= collider.rect.x and
                    snake_segment.rect.x <= collider.rect.x + size):
                return True
        return False

    def is_wall_collision(self, snake_segment, size, width, height):
        if (snake_segment.rect.x >= width or snake_segment.rect.x < 0):
            return True
        if (snake_segment.rect.y >= height or snake_segment.rect.y < 0):
            return True
        return False
